from django.contrib import admin
from .models import Commodity, Asset, Tender
# Register your models here.


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure')


class AssetAdmin(admin.ModelAdmin):
    list_display = ('user', 'commodity', "amount", "time_of_creation")


class TenderAdmin(admin.ModelAdmin):
    list_display = ('pk','user', 'own_commodity', 'own_commodity_ammount',
                    "wish_commodity", "wish_commodity_ammount")


admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Tender, TenderAdmin)
