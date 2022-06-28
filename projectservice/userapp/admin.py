from django.contrib import admin
from userapp.models import *

# Register your models here.
admin.site.register(UserModel)
admin.site.register(LocationModel)
admin.site.register(QuoteModel)
admin.site.register(WalletModel)
admin.site.register(CardModel)

