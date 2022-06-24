from django.urls import path
from .views import *

urlpatterns = [
   path('servicetype/',ServiceTypeVew.as_view()),
   path('servicecity/',ServicecitiesVew.as_view()),
   path('service/',ServiceVew.as_view()),
  
]