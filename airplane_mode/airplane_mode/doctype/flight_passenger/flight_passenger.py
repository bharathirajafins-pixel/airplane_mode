# Copyright (c) 2026, bharathiraja and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		first = self.first_name or ""
		last = self.last_name or ""
		self.full_name = f"{first} {last}".strip()
	pass
