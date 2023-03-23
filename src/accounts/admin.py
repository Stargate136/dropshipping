from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Shopper)
admin.site.register(models.ShippingAddress)
