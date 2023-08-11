from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Group)

admin.site.register(models.Post)
admin.site.register(models.Comment)

admin.site.register(models.Album)

