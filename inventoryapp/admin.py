from django.contrib import admin
from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'unit_price', 'ordering_cost', 'holding_cost',)
    list_display_links = ('stock_name',)
    list_filter = ('stock_name',)
    list_per_page = 20

    # Render filtered options only after 5 characters were entered
    filter_input_length = {
        'stock_name': 5
    }




# Register your models here.
admin.site.register(Inventory, InventoryAdmin)
