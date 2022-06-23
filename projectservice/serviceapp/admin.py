from django.contrib import admin

from serviceapp.models import *

# Register your models here.
admin.site.register(ServiceTypeModel)
admin.site.register(ServiceCitiesModel)
admin.site.register(ServiceModel)
