from django.contrib import admin

# Register your models here.
from Hostmanager.models import UserInfo, Group

admin.register(UserInfo)
admin.register(Group)
