from django.contrib import admin

# Register your models here.

from variable.models import TypeTopic, TypeLocation, TypeYear



class TtypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')

class YtypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')

class LtypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')


admin.site.register(TypeTopic, TtypeAdmin)
admin.site.register(TypeYear, YtypeAdmin)
admin.site.register(TypeLocation, LtypeAdmin)
