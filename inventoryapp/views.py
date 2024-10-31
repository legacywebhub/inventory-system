# IMPORTS
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Inventory
from .utils import *
import numpy as np, matplotlib.pyplot as plt, io, base64
import os, json



########## VARIABLES ###########
# Load data from JSON file
db_path = os.path.join(settings.BASE_DIR, 'db.json')


########## VIEW FUNCTIONS ##########

def index(request):
    with open(db_path, 'r') as file:
        inventory_list = json.load(file)
        inventory_list.reverse()
        print(inventory_list)
        p = Paginator(inventory_list, 5)
        page = request.GET.get('page')
        inventories = p.get_page(page)
    
    context = {
        'inventories': inventories
    }
    return render(request, 'index.html', context)


def inventory(request, id):
    with open(db_path, 'r') as file:
        inventories = json.load(file)

    # Search for the inventory item by id
    inventory_item = next((item for item in inventories if item["id"] == int(id)), None)
    
    # Redirect to home if not found
    if inventory_item is None:
        messages.error(request, 'Inventory item not found!')
        return redirect('home')
    
    return render(request, 'inventory.html', {'inventory': inventory_item})


def add_inventory(request):
    if request.method == 'POST':
        stock_name = request.POST.get('stock_name')
        category = request.POST.get('category')
        initial_quantity = int(request.POST.get('initial_quantity'))
        demand_rate = int(request.POST.get('demand_rate'))
        lead_time = int(request.POST.get('lead_time'))
        unit_price = float(request.POST.get('unit_price'))
        holding_cost = float(request.POST.get('holding_cost'))
        ordering_cost = float(request.POST.get('ordering_cost'))
        # Derived variables
        eoq = calculate_eoq(demand_rate, ordering_cost, holding_cost)
        reorder_level = calculate_reorder_level(demand_rate, lead_time)
        safety_stock = calculate_safety_stock(demand_rate, lead_time)
        order_quantity = calculate_order_quantity(initial_quantity, reorder_level)
        
        # Load existing data from JSON file
        with open(db_path, 'r') as file:
            inventories = json.load(file)
        
        # Determine the new ID
        new_id = inventories[-1]['id'] + 1 if inventories else 1
        
        # Create a new inventory item
        new_inventory = {
            "id": new_id,
            "stock_name": stock_name,
            "category": category,
            "initial_quantity": initial_quantity,
            "reorder_level": reorder_level,
            "safety_stock": safety_stock,
            "lead_time": lead_time,
            "eoq": eoq,
            "order_quantity": order_quantity,
            "demand_rate": demand_rate,
            "holding_cost": holding_cost,
            "ordering_cost": ordering_cost
        }

        print(new_inventory)
        
        # Append the new item to the list
        inventories.append(new_inventory)
        
        # Save updated data back to JSON file
        with open(db_path, 'w') as file:
            json.dump(inventories, file, indent=4)
        
        # Success message and redirect
        messages.success(request, 'Inventory added!')
        return redirect('home')
    
    return render(request, 'add_inventory.html')


def calculate_inventory(request):
    if request.method == 'POST':
        initial_quantity = int(request.POST.get('initial_quantity'))
        demand_rate = int(request.POST.get('demand_rate'))
        lead_time = int(request.POST.get('lead_time'))
        holding_cost = float(request.POST.get('holding_cost'))
        ordering_cost = float(request.POST.get('ordering_cost'))

        # EOQ Calculation
        eoq = calculate_eoq(demand_rate, ordering_cost, holding_cost)
        reorder_level = calculate_reorder_level(demand_rate, lead_time)
        safety_stock = calculate_safety_stock(demand_rate, lead_time)
        order_quantity = calculate_order_quantity(initial_quantity, reorder_level)

        # Generate subplots
        fig, axs = plt.subplots(3, 1, figsize=(8, 10))
        
        # Plot EOQ vs Ordering Cost and Holding Cost
        ordering_costs = np.linspace(10, 200, 100)
        eoq_values = np.sqrt((2 * demand_rate * ordering_costs) / holding_cost)
        axs[0].plot(ordering_costs, eoq_values, label="EOQ")
        axs[0].set_title("EOQ vs Ordering Cost")
        axs[0].set_xlabel("Ordering Cost")
        axs[0].set_ylabel("EOQ")
        axs[0].legend()

        # Plot Reorder Point vs Lead Time
        lead_times = np.linspace(1, 30, 100)
        reorder_levels = demand_rate * lead_times
        axs[1].plot(lead_times, reorder_levels, label="Reorder Point", color="orange")
        axs[1].set_title("Reorder Point vs Lead Time")
        axs[1].set_xlabel("Lead Time (Days)")
        axs[1].set_ylabel("Reorder Point")
        axs[1].legend()

        # Plot Safety Stock vs Lead Time
        safety_stocks = demand_rate * lead_times * 0.5
        axs[2].plot(lead_times, safety_stocks, label="Safety Stock", color="green")
        axs[2].set_title("Safety Stock vs Lead Time")
        axs[2].set_xlabel("Lead Time (Days)")
        axs[2].set_ylabel("Safety Stock")
        axs[2].legend()

        # Save the plot to a string
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        response_data = {
            'eoq': eoq,
            'reorder_level': reorder_level,
            'safety_stock': safety_stock,
            'order_quantity': order_quantity,
            'graph': image_base64,
        }
        return JsonResponse(response_data)

    return render(request, 'calculate_inventory.html')




########## API ##########

def update_parameters(request):
    demand_rate = float(request.GET.get('demand_rate', 0))
    lead_time = float(request.GET.get('lead_time', 0))
    initial_quantity = float(request.GET.get('initial_quantity', 0))
    holding_cost = float(request.GET.get('holding_cost', 0))
    ordering_cost = float(request.GET.get('ordering_cost', 0))

    # Calculating the response variables
    eoq = calculate_eoq(demand_rate, ordering_cost, holding_cost)
    reorder_level = calculate_reorder_level(demand_rate, lead_time)
    order_quantity = calculate_order_quantity(initial_quantity, reorder_level)
    safety_stock = calculate_safety_stock(demand_rate, lead_time)

    return JsonResponse({
        'eoq': eoq,
        'reorder_level': reorder_level,
        'order_quantity': order_quantity,
        'safety_stock': safety_stock,
    })
