from django.urls import path
from .views import *

urlpatterns = [
   path('user/',UserView.as_view()),
   path('userlocation/',LocationView.as_view()),
   path('login/',LoginView.as_view()),
   path('logout/',Logout.as_view()),
   path('whoami/',WhoAmI.as_view()),
   path('quote/',QuoteView.as_view()),
  
]