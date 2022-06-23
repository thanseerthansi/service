from projectservice.globalimport import *
from django.db.models import Q

# Create your views here.
class Companyview(ListAPIView):#2 many 2 many ofields are......
    serializer_class = GetCompanySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(AllowAny,)
    def post(self,request):
        id = self.request.POST.get("id",'')
        try:
            if id:
                if id.isdigit():
                    company_qs = CompanyModel.objects.filter(id=id)  
                    if company_qs.count():
                        company_obj = CompanySerializer(company_qs[0],data=self.request.data,partial=True)
                        msg = "updated successfully"
                    else:return  Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"No Records found with given id"})
                else:return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"provide valid id"})
            else: 
                company_obj = CompanySerializer(data=self.request.data,partial=True)
                msg = "Created successfully"
            company_obj.is_valid(raise_exception=True)
            saved_data = company_obj.save()
            data_city = self.request.POST.get('cities','')
            if data_city :#to add  multiple city datas to many2many
                k=[]
                datac=json.loads(data_city)
                for i in datac:
                    city = ServiceCitiesModel.objects.filter(id=i)
                    if city.count:
                        city_qs = city.first()
                        k.append(city_qs)
                    else : return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id's"})
                saved_data.cities.add(*k)
            data_service = self.request.POST.get('services')
            if data_service : #to add  multiple service datas to many2many
                S=[]
                datas=json.loads(data_service)
                for i in datas:
                    service = ServiceModel.objects.filter(id=i)
                    if service.count:
                        service_qs = service.first()
                        S.append(service_qs)
                    else : return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No Records found with given id's"})
                saved_data.cities.add(*S)
            return Response({"Status":status.HTTP_200_OK,"Message":msg})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            cities = self.request.GET.get("cities")
            qs = CompanyModel.objects.all()
            if id : qs = qs.filter(id=id)
            if cities: qs = qs.filter(cities__in = cities)
            return qs
        except :return None
    def delete(self,request):
        id = self.request.data['id']
        try:
            qs = CompanyModel.objects.filter(id=id)
            if qs.count():
                qs = qs.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No record found"})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e)})
        

class PartnerRegister(ListAPIView):
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
                    password =  self.request.POST.get('password','')
                    if password:
                        msg = "user details and email updated successfully"
                        user_obj = serializer.save(password = make_password(password))
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
            mandatory = ['username','password']
            data = Validate(self.request.data,mandatory)
            if data == True:
                try:
                    serializer = UserSerializer(data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)

                    msg = "Created New User"
                    user_obj = serializer.save(password=make_password(self.request.data['password']),is_partner=True)
                    # print("userserializer",user_obj)
                    return Response({"Status":status.HTTP_200_OK,"Message":msg})
                except Exception as e :
                    return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
            else : return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":data})


class PartnerServiceView(ListAPIView):
    
    serializer_class = PartnerServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    def post(self,request):
        userid = self.request.user.id
        id = self.request.POST.get("id",'')
        partner = self.request.POST.get("partner",'')
        service = self.request.POST.get("service")
        
        try:
            if partner:
                partner_qs = UserModel.objects.filter(id=userid)
                if partner_qs.count():partner_obj = partner_qs.first()
                else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found "})
            if service:
                service_qs = ServiceModel.objects.filter(id=service)
                if service_qs.count():service_obj = service_qs.first()
                else:return Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"Service not found "})
            if id:
                if id.isdigit():
                    partner_service_qs = PartnerServiceModel.objects.filter(id=id)  
                    if partner_service_qs.count():
                        partner_service_qs = partner_service_qs.first()
                        if not service: service_obj=partner_service_qs.service
                        partner_service_obj = PartnerServiceSerializer(partner_service_qs,data=self.request.data,partial=True)
                        msg = "updated successfully"
                    else:return  Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"No Records found with given id"})
                else:return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"provide valid id"})
            else: 
                partner_service_obj = PartnerServiceSerializer(data=self.request.data,partial=True,many=True)
                msg = "Created successfully"
            partner_service_obj.is_valid(raise_exception=True)
            partner_service_obj.save(partnerid=partner_obj,service=service_obj)
            return Response({"Status":status.HTTP_200_OK,"Message":msg})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            id = self.request.GET.get("id",'')
            service_id = self.request.GET.get("service_id",'')
            partner_id = self.request.GET.get("partner",'')
            city = self.request.GET.get("city",'')
            country = self.request.GET.get("country",'')
            quote = self.request.GET.get("quote",'')
            booking = self.request.GET.get("booking",'')
            
            
            qs = PartnerServiceModel.objects.all()
            if id : qs = qs.filter(id=id)
            if service_id: qs = qs.filter(service__id = service_id)
            if partner_id: qs = qs.filter(partnerid__id = partner_id)
            if city: qs = qs.filter(city = city)
            if country: qs = qs.filter(country = country)
            if quote: qs = qs.filter(quote = True)
            if booking: qs = qs.filter(booking = True)
            
            return qs
        except :return None
    def delete(self,request):
        id = self.request.data['id']
        try:
            qs = PartnerServiceModel.objects.filter(id=id)
            if qs.count():
                qs = qs.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No record found"})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e)})
        
class NotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    # def post(self,request):
    #     userid = self.request.user.id
    #     id = self.request.POST.get("id",'')
    #     partner = self.request.POST.get("partner",'')
    #     quote = self.request.POST.get("quote")
        
    #     try:
    #         if partner:
    #             partner_qs = UserModel.objects.filter(service=)
    #             if partner_qs.count():partner_obj = partner_qs.first()
    #             else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found "})
    #         if service:
    #             service_qs = ServiceModel.objects.filter(id=service)
    #             if service_qs.count():service_obj = service_qs.first()
    #             else:return Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"Service not found "})
    #         if id:
    #             if id.isdigit():
    #                 partner_service_qs = PartnerServiceModel.objects.filter(id=id)  
    #                 if partner_service_qs.count():
    #                     partner_service_qs = partner_service_qs.first()
    #                     if not service: service_obj=partner_service_qs.service
    #                     partner_service_obj = PartnerServiceSerializer(partner_service_qs,data=self.request.data,partial=True)
    #                     msg = "updated successfully"
    #                 else:return  Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"No Records found with given id"})
    #             else:return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"provide valid id"})
    #         else: 
    #             partner_service_obj = PartnerServiceSerializer(data=self.request.data,partial=True,many=True)
    #             msg = "Created successfully"
    #         partner_service_obj.is_valid(raise_exception=True)
    #         partner_service_obj.save(partnerid=partner_obj,service=service_obj)
    #         return Response({"Status":status.HTTP_200_OK,"Message":msg})
    #     except Exception as e:
    #         return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):
        try:
            userid = self.request.user.id
            is_admin = self.request.user.is_admin
            is_partner = self.request.user.is_partner
            id = self.request.GET.get("id",'')
            quote = self.request.GET.get("quote",'')
            if userid:
                if is_admin == True: qs= NotificationModel.objects.all()
                else: qs = NotificationModel.objects.filter(partnerid__in=userid)
                
                if qs.count():
                    if id : qs = qs.filter(id=id)
                    if quote : qs = qs.filter(quote__id=quote)
                    return qs
                else:return None
            else: return None
            
        except :return None
    def delete(self,request):
        id = self.request.data['id']
        try:
            qs = PartnerServiceModel.objects.filter(id=id)
            if qs.count():
                qs = qs.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No record found"})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e)})


class AcceptedQuoteView(ListAPIView):
    serializer_class = AcceptedQuoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    def post(self,request):
        userid = self.request.user.id
        id = self.request.POST.get("id",'')
        partner = self.request.POST.get("partner",'')
        quote = self.request.POST.get("quote")
        
        try:
            if partner:
                partner_qs = UserModel.objects.filter(id=userid)
                if partner_qs.count():partner_obj = partner_qs.first()
                else: return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"User not found "})
            if quote:
                quote_qs = QuoteModel.objects.filter(id=quote)
                if quote_qs.count():
                    quote_obj = quote_qs.first()
                else:return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"quote not found"})
            if id:
                if id.isdigit():
                    accepted_qs = AcceptedQuoteModel.objects.filter(id=id)  
                    if accepted_qs.count():
                        accepted_qs = accepted_qs.first()
                        if not quote: quote_obj=accepted_qs.quote
                        if not partner: partner_obj=accepted_qs.partnerid
                        accepted_obj = AcceptedQuoteSerializer(accepted_qs,data=self.request.data,partial=True)
                        msg = "updated successfully"
                    else:return  Response({"Status":status.HTTP_404_NOT_FOUND,"Messsage":"No Records found with given id"})
                else:return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":"provide valid id"})
            else: 
                accepted_obj = AcceptedQuoteSerializer(data=self.request.data,partial=True)
                msg = "Created successfully"
            accepted_obj.is_valid(raise_exception=True)
            accepted_obj.save(partnerid=partner_obj,quote=quote_obj)
            return Response({"Status":status.HTTP_200_OK,"Message":msg})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e),})
    def get_queryset(self):#to edit frm here 
        try:
            userid = self.request.user.id
            is_admin = self.request.user.is_admin
            is_partner = self.request.user.is_partner
            id = self.request.GET.get("id",'')
            quote = self.request.GET.get("quote",'')
            qs = AcceptedQuoteModel.objects.all()  
            if is_admin == True: qs = qs
            elif is_partner == True: qs = qs.filter(partnerid=userid)
            else : qs=qs.filter(quote__userid__id = userid )
              
            
            if id : qs = qs.filter(id=id)
            if quote : qs = qs.filter(quote__id=quote)
            return qs
        
            
        except :return None
    def delete(self,request):
        id = self.request.data['id']
        try:
            qs = PartnerServiceModel.objects.filter(id=id)
            if qs.count():
                qs = qs.delete()
                return Response({"Status":status.HTTP_200_OK,"Message":"deleted successfully"})
            return Response({"Status":status.HTTP_404_NOT_FOUND,"Message":"No record found"})
        except Exception as e:
            return Response({"Status":status.HTTP_400_BAD_REQUEST,"Message":str(e)})