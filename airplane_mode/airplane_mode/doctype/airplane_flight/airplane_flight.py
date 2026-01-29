# Copyright (c) 2026, bharathiraja
# License: see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
    website = frappe._dict(
        condition_field="is_published"
    )

    def get_context(self, context):
        if not self.is_published:
            frappe.throw("Not Found", frappe.DoesNotExistError)

        context.doc = self
        context.no_cache = 1

        if self.duration:
            total_seconds = int(self.duration)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            context.formatted_duration = f"{hours}h {minutes}m"
        else:
            context.formatted_duration = "0h 0m"

    def validate(self):
        if self.source_airport == self.destination_airport:
            frappe.throw("Source and Destination airports cannot be the same")

        if self.source_airport_code and self.destination_airport_code:
            self.route = f"{self.source_airport_code} → {self.destination_airport_code}"

    def on_update(self):
        """
        Trigger background job when gate changes
        """
        if self.has_value_changed("gate"):
            frappe.enqueue(
                method="airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_in_tickets",
                queue="long",
                flight_name=self.name,
                new_gate_number=self.gate,
                after_commit=True
            )

    def on_submit(self):
        self.db_set("status", "Completed", update_modified=False)

    def on_cancel(self):
        self.db_set("status", "Cancelled", update_modified=False)


def update_gate_number_in_tickets(flight_name, new_gate_number):
    """
    Background job:
    Update gate_number in all tickets linked to this flight
    """
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight_name},
        pluck="name"
    )

    for ticket in tickets:
        frappe.db.set_value(
            "Airplane Ticket",
            ticket,
            "gate_number",
            new_gate_number,
            update_modified=False
        )

    frappe.db.commit()


@frappe.whitelist()
def get_flight_price(flight_name):
    flight = frappe.get_doc("Airplane Flight", flight_name)
    airplane = frappe.get_doc("Airplane", flight.airplane)
    return airplane.flight_price
