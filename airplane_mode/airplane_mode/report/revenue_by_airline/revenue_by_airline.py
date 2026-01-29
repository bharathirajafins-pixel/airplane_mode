import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum, Coalesce
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data, total_revenue = get_data()
    chart = get_chart(data)
    summary = get_summary(total_revenue)

    return columns, data, None, chart, summary


def get_columns():
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200,
        },
        {
            "label": _("Revenue"),
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def get_data():
    Ticket = DocType("Airplane Ticket")
    Flight = DocType("Airplane Flight")
    Airplane = DocType("Airplane")

    # Query Builder - Join tables to get airline with revenue
    query = (
        frappe.qb.from_(Ticket)
        .join(Flight).on(Ticket.flight == Flight.name)
        .join(Airplane).on(Flight.airplane == Airplane.name)
        .select(
            Airplane.airline,
            Sum(Ticket.total_amount).as_("revenue"),
        )
        .where(Ticket.docstatus == 1)
        .groupby(Airplane.airline)
    )

    results = query.run(as_dict=True)

    # Get ALL airlines (including those with zero revenue)
    all_airlines = frappe.get_all("Airline", pluck="name")
    revenue_map = {airline: 0.0 for airline in all_airlines}

    # Update with actual revenues
    total_revenue = 0.0
    for row in results:
        revenue_map[row.airline] = float(row.revenue or 0)
        total_revenue += float(row.revenue or 0)

    # Build final data - ONLY airline rows, NO total row
    data = []
    for airline in sorted(revenue_map.keys()):  # Sort alphabetically
        data.append({
            "airline": airline,
            "revenue": revenue_map[airline],
        })

    # DO NOT add total row to data - it goes in summary only
    return data, total_revenue


def get_chart(data):
    labels = []
    values = []

    for row in data:
        labels.append(row["airline"])
        values.append(row["revenue"])

    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}],
        },
        "type": "donut",
    }


def get_summary(total_revenue):
    return [
        {
            "label": _("Total Revenue"),
            "value": total_revenue,
            "datatype": "Currency",
        }
    ]