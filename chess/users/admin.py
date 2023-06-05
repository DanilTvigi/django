from django.contrib import admin
from .models import SessionConnection, CustomUser

admin.site.register(SessionConnection)
admin.site.register(CustomUser)
