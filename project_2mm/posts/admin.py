from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Group)
admin.site.register(models.Album)