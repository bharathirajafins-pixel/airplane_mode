import frappe

def get_context(context):
    # Read URL parameters
    context.flight = frappe.form_dict.get("flight")
    context.price = frappe.form_dict.get("price")
