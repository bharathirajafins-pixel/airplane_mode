# Copyright (c) 2026, bharathiraja and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirplaneTicket(WebsiteGenerator):
    # -----------------------------
    # UI Indicator (Status Colors)
    # -----------------------------
    def get_indicator(self):
        if self.status == "Booked":
            return ("Booked", "gray")
        elif self.status == "Checked-In":
            return ("Checked-In", "purple")
        elif self.status == "Boarded":
            return ("Boarded", "green")
        return (self.status, "blue")

    # -----------------------------
    # Validation
    # -----------------------------
    def validate(self):
        self.remove_duplicate_addons()
        self.calculate_total_amount()

    # -----------------------------
    # Amount Calculation
    # -----------------------------
    def calculate_total_amount(self):
        addons_total = sum(
            (row.amount or 0) for row in (self.add_ons or [])
        )

        self.total_amount = (self.flight_price or 0) + addons_total

    # -----------------------------
    # Remove Duplicate Add-ons
    # -----------------------------
    def remove_duplicate_addons(self):
        seen_items = set()
        unique_rows = []

        for row in (self.add_ons or []):
            if row.item not in seen_items:
                seen_items.add(row.item)
                unique_rows.append(row)

        self.set("add_ons", unique_rows)

    # -----------------------------
    # Before Insert
    # -----------------------------
    def before_insert(self):
        self.assign_seat()
        self.validate_airplane_capacity()

    # -----------------------------
    # Seat Assignment
    # -----------------------------
    def assign_seat(self):
        number = random.randint(1, 99)
        letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{number}{letter}"

    # -----------------------------
    # Capacity Validation
    # -----------------------------
    def validate_airplane_capacity(self):
        # Get flight
        flight = frappe.get_doc("Airplane Flight", self.flight)

        # Get airplane
        airplane = frappe.get_doc("Airplane", flight.airplane)

        capacity = airplane.capacity

        # Count existing tickets (Draft + Submitted)
        booked_tickets = frappe.db.count(
            "Airplane Ticket",
            {
                "flight": self.flight,
                "docstatus": ["<", 2]
            }
        )

        if booked_tickets >= capacity:
            frappe.throw(
                f"No seats available for this flight.<br>"
                f"Capacity: {capacity}<br>"
                f"Already Booked: {booked_tickets}"
            )

    # -----------------------------
    # Submission Rule
    # -----------------------------
    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw(
                "You can submit the ticket only when status is Boarded"
            )
