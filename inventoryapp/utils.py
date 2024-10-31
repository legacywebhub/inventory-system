import numpy as np

'''
Daily demand rate = demand rate / 30
'''

# Utility functions to calculate response variables

def calculate_eoq(demand_rate, ordering_cost, holding_cost):
    # Adjust demand rate to daily
    daily_demand_rate = demand_rate
    return int(np.sqrt((2 * daily_demand_rate * ordering_cost) / holding_cost))

def calculate_reorder_level(demand_rate, lead_time):
    # Adjust demand rate to daily
    daily_demand_rate = demand_rate
    return int(daily_demand_rate * lead_time)

def calculate_order_quantity(initial_quantity, reorder_level):
    return int(max(0, reorder_level - initial_quantity))

def calculate_safety_stock(demand_rate, lead_time):
    # Adjust demand rate to daily
    daily_demand_rate = demand_rate
    return int(daily_demand_rate * lead_time * 0.5)