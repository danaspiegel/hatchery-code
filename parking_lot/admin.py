from django.contrib import admin

from models import Lot, Spot

class LotAdmin(admin.ModelAdmin):
    list_display = ('name', 'lot_type', 'spot_count', 'open_time', 'close_time', 
                    'hourly_rate', 'monthly_rate', )
    list_filter = ('lot_type', )
    prepopulated_fields = { 'slug': ('name', ) }

admin.site.register(Lot, LotAdmin)


class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'lot', 'level', 'size', )
    list_filter = ('level', 'size', 'lot', )
    
    

admin.site.register(Spot, SpotAdmin)
