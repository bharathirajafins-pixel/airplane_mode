import frappe

def get_context(context):
    context.shops = frappe.get_all(
        "Airport Shop",
        filters={
            "is_published": 1,
            "status": "Available"
        },
        fields=[
            "name",
            "shop_number",
            "shop_name",
            "airport",
            "area",
            "status"
        ]
    )
