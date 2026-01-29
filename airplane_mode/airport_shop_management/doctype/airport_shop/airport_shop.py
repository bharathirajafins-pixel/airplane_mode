# Copyright (c) 2026, bharathiraja and contributors
# For license information, please see license.txt



# Copyright (c) 2026, bharathiraja
# License: see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):

    def after_insert(self):
        self.update_airport_counts()

    def on_update(self):
        self.update_airport_counts()

    def on_trash(self):
        self.update_airport_counts()

    def update_airport_counts(self):
        if not self.airport:
            return

        total = frappe.db.count(
            "Airport Shop",
            filters={"airport": self.airport}
        )

        occupied = frappe.db.count(
            "Airport Shop",
            filters={
                "airport": self.airport,
                "status": "Occupied"
            }
        )

        available = max(total - occupied, 0)

        frappe.db.set_value(
            "Airport",
            self.airport,
            {
                "total_shops": total,
                "occupied_shops": occupied,
                "available_shops": available
            }
        )
