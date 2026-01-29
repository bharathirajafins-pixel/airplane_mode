import frappe

def get_context(context):
    context.no_cache = 1
    
    # Show all published flights
    flights = frappe.get_all(
        "Airplane Flight",
        filters={"is_published": 1},
        fields=[
            "name",
            "route",
            "source_airport_code",
            "destination_airport_code",
            "date_of_departure",
            "time_of_departure",
            "duration",
            "airplane",
            "price"
        ],
        order_by="date_of_departure asc"
    )
    
    # Format the data before passing to template
    for flight in flights:
        if flight.get("price"):
            flight["formatted_price"] = frappe.utils.fmt_money(flight.price)
        else:
            flight["formatted_price"] = "N/A"
            
        if flight.get("duration"):
            flight["formatted_duration"] = frappe.utils.format_duration(flight.duration)
        else:
            flight["formatted_duration"] = "N/A"
    
    context.flights = flights