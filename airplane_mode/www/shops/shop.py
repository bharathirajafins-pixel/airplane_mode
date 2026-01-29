import frappe

def get_context(context):
    shop_name = frappe.form_dict.get("shop")

    if not shop_name:
        frappe.throw("Shop not specified", frappe.DoesNotExistError)

    shop = frappe.get_all(
        "Airport Shop",
        filters={"shop_name": shop_name},
        limit=1
    )

    if not shop:
        frappe.throw(f"Airport Shop '{shop_name}' not found", frappe.DoesNotExistError)

    context.shop = frappe.get_doc("Airport Shop", shop[0].name)
