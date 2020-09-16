from django.contrib import admin
from billing.models import Transaction, PriceToDays




class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'price', 'transaction_id', 'timestamp', 'startdate', 'enddate', 'description')
    search_fields = ['transaction_id']
    list_filter = ('timestamp', 'price')

    def __str__(self,obj):
        return obj.__str__()

class PriceToDaysAdmin(admin.ModelAdmin):
    list_display = ('id','label','cashprice','daystoadd','subplan','discount','active')

    def __str__(self,obj):
        return obj.__str__()

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PriceToDays, PriceToDaysAdmin)

