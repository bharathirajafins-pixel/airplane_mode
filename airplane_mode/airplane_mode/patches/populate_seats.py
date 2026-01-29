import frappe
import random

def execute():
    """
    Populate seat field for existing Airplane Ticket records
    where seat is not set.
    """

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"seat": ["in", ["", None]]},
        pluck="name"
    )

    for ticket_name in tickets:
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        seat = f"{seat_number}{seat_letter}"

        frappe.db.set_value(
            "Airplane Ticket",
            ticket_name,
            "seat",
            seat
        )

    frappe.db.commit()
