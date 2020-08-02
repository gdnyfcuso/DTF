from django.contrib import admin
from .models import FDT_Account,FDT_User,FDT_User_Fund,FDT_UserOpHistory
# Register your models here.
admin.register(FDT_Account)
admin.register(FDT_User)
admin.register(FDT_User_Fund)
admin.register(FDT_UserOpHistory)