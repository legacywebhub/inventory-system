# inventory/models.py
from django.db import models
from .utils import *

class Inventory(models.Model):
    stock_name = models.CharField(max_length=60, null=False, blank=False, unique=True)
    initial_quantity = models.IntegerField()
    lead_time_days = models.IntegerField()
    demand_rate = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def order_quantity(self):
        return calculate_order_quantity(self.initial_quantity, self.reorder_level)
    
    @property
    def eoq(self):
        return calculate_eoq(self.demand_rate, self.ordering_cost, self.holding_cost)
    
    @property
    def reorder_level(self):
        return calculate_reorder_level(self.demand_rate, self.lead_time_days)
    
    @property
    def safety_stock(self):
        return calculate_safety_stock(self.demand_rate, self.lead_time_days)
    