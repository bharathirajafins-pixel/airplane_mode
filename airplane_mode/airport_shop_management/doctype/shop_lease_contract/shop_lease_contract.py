# Copyright (c) 2026, bharathiraja
# License: MIT

import frappe
from frappe.utils import today, getdate
from frappe.model.document import Document


class ShopLeaseContract(Document):
    pass


def send_monthly_rent_reminders():
    settings = frappe.get_single("Airport Shop Settings")

    # Stop if reminders disabled
    if not settings.enable_rent_reminder:
        return

    today_date = getdate(today())

    contracts = frappe.get_all(
        "Shop Lease Contract",
        filters={
            "is_active": 1
        },
        fields=[
            "name",
            "tenant",
            "rent_amount",
            "start_date"
        ]
    )

    for contract in contracts:
        if not contract.contract_start_date:
            continue

        start_date = getdate(contract.contract_start_date)

        # Monthly reminder based on start date DAY
        if today_date.day != start_date.day:
            continue

        tenant_email = frappe.db.get_value(
            "Tenant",
            contract.tenant,
            "email"
        )

        if not tenant_email:
            continue

        # PROOF LOG (temporary)
        frappe.log_error(
            title="RENT REMINDER TRIGGERED",
            message=contract.name
        )

        frappe.sendmail(
            recipients=[tenant_email],
            subject="Monthly Rent Due Reminder",
            message=f"""
            Dear Tenant,<br><br>

            This is a reminder that your monthly rent of
            <b>{contract.rent_amount}</b> is due.<br><br>

            Lease Contract: {contract.name}<br><br>

            Regards,<br>
            Airport Management
            """
        )
