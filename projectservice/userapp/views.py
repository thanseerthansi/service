
from projectservice.globalimport import *
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.geos import GEOSGeometry


# Create your views here.
class UserView(ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(AllowAny,)
    
    def get_queryset(self):
        try:
            user = self.request.GET.get("user",'')#any value to filter the user data only
            partner = self.request.GET.get("partner",'')#any value to filter all  partners
            userid = self.request.user.id
            qs = UserModel.objects.all()
            if user: qs = qs.filter(id=userid)
            if partner: qs = qs.filter(is_partner=True)
            return qs
        except Exception as e:
            # print("euser",e)
            return None

    def post(self,request):
        userobj = ""
        id = self.request.POST.get("id","")
        if id:
            if id.isdigit():
                try:
                    user = UserModel.objects.filter(id=id)
                    if user.count():
                        user = user.first()
                    else:return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found"})
                    serializer = UserSerializer(user,data=request.data,partial= True)
                    serializer.is_valid(raise_exception=True)
                    email =  self.request.POST.get('email','')
                    if email:
                        msg = "user details and email updated successfully"
                        user_obj = serializer.save(password = make_password(email))
                    else: 
                        msg = "User details updated successfully"
                        user_obj = serializer.save()
                  
                    return Response({"Status":status.HTTP_200_OK,"Message":msg})
                except Exception as e:
                    # print(f"Exception occured{e}")
                    if  user_obj : user_obj.delete()
                    else : pass
                    return  Response({
                        "Status":status.HTTP_400_BAD_REQUEST,
                        "Message":f"Excepction occured {e}"
                    })
            else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"Please provide valid user"})
        else:
            # print("id2",id)
            mandatory = ['username','email']
            data = Validate(self.request.data,mandatory)
            if data == True:
                try:
                    serializer = UserSerializer(data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)

                    msg = "Created New User"
                    user_obj = serializer.save(password=make_password(self.request.data['email']))
                    # print("userserializer",user_obj)
                    return Response({"Status":status.HTTP_200_OK,"Message":msg})
                except Exception as e :
                    return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
            else : return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":data})
    def delete(self,request):
        # isadmin = self.request.user.is_admin
        # superuser = self.request.user.is_superuser
        # if isadmin==True or superuser == True:
        try:
            id = self.request.data['id']
            u_obj = UserModel.objects.filter(id=id)
            if u_obj.count():
                # print("obj",u_obj)
                u_obj.delete()
        
                return Response({"status":status.HTTP_200_OK,"message":"deleted successfully"})
            else: return Response({"status":status.HTTP_404_NOT_FOUND,"message":"No records with given id" })
            
        except Exception as e:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(e),})
        # else: return Response({"Status":False,"Message":"Something went wrong"})
            
class WhoAmI(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self,request):
        try:
            return Response({
                "Status":1,
                "Data":self.request.user.username   
            })
        except Exception as e: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})


        
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # print("data",self.request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # print(serializer)
        try:
            test = serializer.is_valid(raise_exception=True) 
            user = serializer.validated_data['user']
            
            token, created = Token.objects.get_or_create(user=user)
            # print("token",token.key)
            return Response({
                "Status":status.HTTP_200_OK,
                'token': "Token "+token.key,
                'user_id': user.pk,
                'username': user.username,
                'is_superuser':user.is_superuser,
            })
        except Exception as e:
            # print("e",e)
            return Response({
                "Status":status.HTTP_400_BAD_REQUEST,
                "Message":"Incorrect Username or Password",
                "excepction":str(e),
            })
class Logout(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
  
    def get(self,request):
        try:
            Data = Token.objects.get(user = self.request.user.id)
            Data.delete()
            # print("ok")
            return Response({"Status":status.HTTP_200_OK,"Message":"logout successfully"})
        except Exception as e:
            # print("e",e)
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e)})


class LocationView(ListAPIView):
    serializer_class = LocaionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(AllowAny,)
    def post(self,request):
        try:
            mandatory = ['place','area','street_no','appartment_no']
            data = Validate(self.request.data,mandatory)
            id = self.request.POST.get("id","")   
            userid = self.request.user.id 
            lat = self.request.POST.get("latitude","")
            lon = self.request.POST.get("longitude","")   
            location = ""       
            if userid != None:
                user_qs = UserModel.objects.filter(id=userid)
                if user_qs.count(): user_obj = user_qs.first()  
            else :return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found please login"})    
            if lat!="" and lon !="":
                    location =GEOSGeometry(Point(float(lon), float(lat),srid=4326))       
            if id: 
                if id.isdigit():
                    location_qs = LocationModel.objects.filter(id=id)
                    if location_qs.count():
                        location_qs = location_qs.first()
                        location_obj = LocaionSerializer(location_qs,data=self.request.data,partial=True)
                        msg = "Successfully modified"
                    else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id"})
                else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"Provide valid id"}) 
            else: 
                if data == True:
                    location_obj = LocaionSerializer(data=self.request.data,partial=True)
                    msg = "Successfully Created" 
                else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":data})          
            location_obj.is_valid(raise_exception=True)
            location_obj.save(user=user_obj,location=location )
            return Response({"Status":status.HTTP_200_OK,"Message":msg})                
        except Exception as e: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            area =self.request.GET.get("area",'')
            user = self.request.GET.get("user",'')#to get the user data only
            userid = self.request.user.id
            qs = LocationModel.objects.all().select_related('user')
            if id : qs = qs.filter(id=id)
            if area : qs = qs.filter(area=area)
            if user : qs = qs.filter(user__id=userid)
            return qs
        except :return None
 
    def delete(self,request):
        try:
            id = self.request.data['id']
            # id = json.loads(id)
            objects = LocationModel.objects.filter(id=id)
            if objects.count():
                objects.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No records with given id"})
        except Exception as e:
            return Response({
                "Status" : status.HTTP_400_BAD_REQUEST,
                "Message" : str(e),
            })
        

class QuoteView(ListAPIView):
   
    serializer_class = QuoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    def post(self,request):
        try:
            
            id = self.request.POST.get("id","")  
            service = self.request.POST.get("service",'')
            if service:
                service_qs = ServiceModel.objects.filter(id=service)
                if service_qs.count():
                    service_qs = service_qs.first()
                else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"provide valid id"})
            userid = self.request.user.id     
            if userid != None:
                user_qs = UserModel.objects.filter(id=userid)
                if user_qs.count(): user_obj = user_qs.first()           
            if id: 
                if id.isdigit():
                    quote_qs = QuoteModel.objects.filter(id=id)
                    if quote_qs.count():
                        quote_qs = quote_qs.first()
                        if not service: service_qs = quote_qs.service
                        quote_obj = QuoteSerializer(quote_qs,data=self.request.data,partial=True)
                        msg = "Successfully modified"
                    else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id"})
                else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"Provide valid id"}) 
            else: 
                quote_obj = QuoteSerializer(data=self.request.data,partial=True)
                # print("dara",self.request.data)
                msg = "Successfully Created"  
            quote_obj.is_valid(raise_exception=True)
            saved_data = quote_obj.save(userid=user_obj,service=service_qs )
            # print("savde",saved_data)
            #notificationModel create
            # print("service_qs",service_qs)
            if service_qs:#adding to notification
                if saved_data.is_booking != True:
                    # print("okkk")
                    partner_service_qs = PartnerServiceModel.objects.filter(service=service_qs)
                    # print("partnerqson",partner_service_qs)
                    if partner_service_qs.count():
                        notification_obj = NotificationModel.objects.create(quote=saved_data)
                        # print("Notification_obj",notification_obj)
                        p=[]
                        for i in partner_service_qs:
                            
                            Email_address = i.partnerid.email
                            name = i.partnerid.username
                            p.append(i.partnerid)
                            try:
                                msg_html = render_to_string('email2.html', {'email': Email_address, 'name': name})
                                # print('email',msg_html)
                                send_mail(
                                    'congratulation  -'+str(name),
                                    'thanks',
                                    'gymmanagment720@gmail.com',
                                    [Email_address],
                                    fail_silently=False,
                                    html_message = msg_html,
                                )
                                print("email success",i.partnerid.email)
                            except:
                                print("email failed",i.partnerid.email)
                                pass
                        notification_obj.partnerid.add(*p)
                    else:
                        saved_data.delete()
                        return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"given service not provided in your area"})
                else:
                    print("booking") 
                    admin_qs =  UserModel.objects.filter(Q(is_admin=True) | Q(is_superuser=True))
                    print("userqs",admin_qs)
                    partner_service_qs = PartnerServiceModel.objects.filter(service=service_qs)
                    if partner_service_qs.count():
                        notification_obj = NotificationModel.objects.create(quote=saved_data)
                        if admin_qs.count():
                            a=[]
                            for i in admin_qs:
                                a.append(i)
                            notification_obj.partnerid.add(*a)
                    else:
                        saved_data.delete()
                        return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"given service not provided in your area"})
                            


                    
            return Response({"Status":status.HTTP_200_OK,"Message":msg})                
        except Exception as e: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            service =self.request.GET.get("service",'')
            user = self.request.GET.get("user",'')#to get the user data only
            userid = self.request.user.id
            location = self.request.GET.get("location",'')
            qs = QuoteModel.objects.all()
            if id : qs = qs.filter(id=id)
            if service : qs = qs.filter(srvice__service_name=service)
            if location : qs = qs.filter(service_location=location)
            if user: qs=qs.filter(userid__id=userid)
            return qs
        except :return None
 
    def delete(self,request):
        try:
            id = self.request.data['id']
            # id = json.loads(id)
            objects = QuoteModel.objects.filter(id=id)
            if objects.count():
                objects.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No records with given id"})
        except Exception as e:
            return Response({
                "Status" : status.HTTP_400_BAD_REQUEST,
                "Message" : str(e),
            })

class WalletView(ListAPIView):
    serializer_class = WalletSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    def post(self,request):
        try:
            # mandatory = ['balance']
            # data = Validate(self.request.data,mandatory)
            id = self.request.POST.get("id","")   
            userid = self.request.user.id        
            if userid != None:
                user_qs = UserModel.objects.filter(id=userid)
                if user_qs.count(): user_obj = user_qs.first()  
            else :return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found please login"})   
            if id: 
                if id.isdigit():
                    wallet_qs = WalletModel.objects.filter(id=id)
                    if wallet_qs.count():
                        wallet_qs = wallet_qs.first()
                        wallet_obj = WalletModel(wallet_qs,data=self.request.data,partial=True)
                        msg = "Successfully modified"
                        
                    else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id"})
                else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"Provide valid id"}) 
            else: 
                # if data == True:
                wallet_obj = WalletSerializer(data=self.request.data,partial=True)
                msg = "Successfully Created" 
                # else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":data}) 
            wallet_obj.is_valid(raise_exception=True)
            wallet_obj.save(user=user_obj )
            return Response({"Status":status.HTTP_200_OK,"Message":msg})                
        except Exception as e: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            user = self.request.GET.get("user",'')#to get the user data only
            userid = self.request.user.id
            getuser = self.request.GET.get("userid")
            qs = WalletModel.objects.all().select_related('user')
            if getuser: qs = qs.filter(user__id=getuser)
            if id : qs = qs.filter(id=id)
            if user : qs = qs.filter(user__id=userid)
            return qs
        except :return None
 
    def delete(self,request):
        try:
            id = self.request.data['id']
            # id = json.loads(id)
            objects = WalletModel.objects.filter(id=id)
            if objects.count():
                objects.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No records with given id"})
        except Exception as e:
            return Response({
                "Status" : status.HTTP_400_BAD_REQUEST,
                "Message" : str(e),
            })


class CardView(ListAPIView):
    serializer_class = CardSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    def post(self,request):
        try:
            mandatory = ['card_no','name_of_card','valid_thru','cvv']
            data = Validate(self.request.data,mandatory)
            id = self.request.POST.get("id","")   
            userid = self.request.user.id        
            if userid != None:
                user_qs = UserModel.objects.filter(id=userid)
                if user_qs.count(): user_obj = user_qs.first()  
            else :return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found please login"})   
            # if id: 
            #     if id.isdigit():
            #         wallet_qs = WalletModel.objects.filter(id=id)
            #         if wallet_qs.count():
            #             wallet_qs = wallet_qs.first()
            #             wallet_obj = WalletModel(wallet_qs,data=self.request.data,partial=True)
            #             msg = "Successfully modified"
                        
            #         else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id"})
            #     else: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"Provide valid id"}) 
            # else: 
            # if data == True:
            card_list = list(CardModel.objects.filter(user=userid).values_list('user',flat=True))
            # print("card",card_list)
            # print("carduser",user_obj.id)
            if user_obj.id in card_list: 
                card_qs= CardModel.objects.filter(user=userid)
                if card_qs.count():
                    card_qs = card_qs.first()
                    card_obj = CardSerializer(card_qs,data=self.request.data,partial=True)
                    msg = "updated successfully"
                else:return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"card not found"})
            else:
                card_obj = CardSerializer(data=self.request.data,partial=True)
                msg = "Successfully Created" 
            # else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":data}) 
            card_obj.is_valid(raise_exception=True)
            card_obj.save(user=user_obj)
            return Response({"Status":status.HTTP_200_OK,"Message":msg})                
        except Exception as e: return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            # user = self.request.GET.get("user",'')#to get the user data only
            userid = self.request.user.id
            qs = CardModel.objects.filter(user__id=userid).select_related('user')
            if id : qs = qs.filter(id=id)
            # if user : qs = qs.filter(user__id=userid)
            return qs
        except :return None
 
    def delete(self,request):
        try:
            id = self.request.data['id']
            # id = json.loads(id)
            objects = CardModel.objects.filter(id=id)
            if objects.count():
                objects.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No records with given id"})
        except Exception as e:
            return Response({
                "Status" : status.HTTP_400_BAD_REQUEST,
                "Message" : str(e),
            })
