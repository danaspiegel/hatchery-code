from django.contrib import admin

from models import Address, Person

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)

class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
