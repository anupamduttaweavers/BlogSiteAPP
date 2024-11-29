from django.contrib import admin
from . import models

admin.site.register(models.Account)
admin.site.register(models.Session)
admin.site.register(models.OTP)


# Register your models here.
