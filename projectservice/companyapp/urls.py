from django.urls import path
from .views import *

urlpatterns = [
   path('company/',Companyview.as_view()),
   path('partnerregister/',PartnerRegister.as_view()),
   path('partnerservice/',PartnerServiceView.as_view()),
   path('notification/',NotificationView.as_view()),
   path('acceptedquote/',AcceptedQuoteView.as_view()),
  
]