from django.contrib import admin

from companyapp.models import *

# Register your models here.
admin.site.register(CompanyModel)
admin.site.register(PartnerServiceModel)
admin.site.register(NotificationModel)
admin.site.register(AcceptedQuoteModel)