import frappe

def get_context(context):
    context.no_cache = 1
    
    flight_name = frappe.form_dict.get("flight")
    
    if not flight_name:
        frappe.throw("Flight not specified")
    
    try:
        doc = frappe.get_doc("Airplane Flight", flight_name)
        
        if not doc.is_published:
            frappe.throw("Flight not found or not available")
        
        context.doc = doc
        
        # Safely format price
        if doc.price:
            context.formatted_price = frappe.utils.fmt_money(doc.price)
        else:
            context.formatted_price = "Price not available"
        
        # Safely format duration
        if doc.duration:
            context.formatted_duration = frappe.utils.format_duration(doc.duration)
        else:
            context.formatted_duration = "Duration not available"
            
        # Get airline name safely
        if doc.airplane:
            context.airline_name = frappe.db.get_value("Airplane", doc.airplane, "airline") or doc.airplane
        else:
            context.airline_name = "N/A"
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Flight Page Error")
        frappe.throw("Flight not found")