from django.contrib import admin

# Register your models here.

from .models import Brand, Tech, Shoe

#admin.site.register(Brand)
#admin.site.register(Tech)
#admin.site.register(Shoe)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
admin.site.register(Brand, BrandAdmin)

class TechAdmin(admin.ModelAdmin):
    list_display = ('name', 'foamType')
admin.site.register(Tech, TechAdmin)



class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'date_of_model', 'lockdown', 'traction', 'comfort', 'looks', 'display_tech')
    list_filter = ('brand', 'lockdown', 'traction', 'comfort', 'looks', 'tech')
admin.site.register(Shoe, ShoeAdmin)

