from django.contrib import admin

from .models import Basket, Item, Event, CurrentEvent, Vendor

# Register your models here.
admin.site.register(Basket)
admin.site.register(Item)
admin.site.register(Event)
admin.site.register(CurrentEvent)
admin.site.register(Vendor)

