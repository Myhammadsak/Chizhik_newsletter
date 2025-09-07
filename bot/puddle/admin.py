from django.contrib import admin
from .models import CustomUser, Groups, Newsletter

admin.site.register(CustomUser)
admin.site.register(Groups)
admin.site.register(Newsletter)