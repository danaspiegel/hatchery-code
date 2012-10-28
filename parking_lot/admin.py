from django.contrib import admin

from models import Lot, Spot

class LotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lot, LotAdmin)

class SpotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Spot, SpotAdmin)
