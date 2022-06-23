from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
import json

from userapp.models import UserModel
from userapp.serializers import *
from projectservice.validation import Validate
from rest_framework import status
from serviceapp.models import *
from serviceapp.serializers import *
from companyapp.models import *
from companyapp.serializers import *