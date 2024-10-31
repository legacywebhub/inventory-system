// Function to update the output fields
function updateParameters() {
    const demandRate = document.getElementById("demand_rate").value || 0;
    const leadTime = document.getElementById("lead_time").value || 0;
    const initialQuantity = document.getElementById("initial_quantity").value || 0;
    const holdingCost = document.getElementById("holding_cost").value || 0;
    const orderingCost = document.getElementById("ordering_cost").value || 0;

    // Sending AJAX request to the Django backend
    fetch(`/update_parameters/?demand_rate=${demandRate}&lead_time=${leadTime}&initial_quantity=${initialQuantity}&holding_cost=${holdingCost}&ordering_cost=${orderingCost}`)
        .then(response => response.json())
        .then(data => {
            // Updating the output fields with the response data
            document.getElementById("eoq").textContent = data.eoq.toFixed(2);
            document.getElementById("reorder_point").textContent = data.reorder_point.toFixed(2);
            document.getElementById("order_quantity").textContent = data.order_quantity.toFixed(2);
            document.getElementById("safety_stock").textContent = data.safety_stock.toFixed(2);
        })
        .catch(error => console.error('Error:', error));
}

// Adding event listeners to the input fields for real-time updates
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', updateParameters);
});
