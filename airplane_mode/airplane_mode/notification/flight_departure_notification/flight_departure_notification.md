<p>Flight {{ doc.name }} will depart in 24 hours.</p>

<p>
Route: {{ doc.source_airport_code }} → {{ doc.destination_airport_code }}<br>
Date: {{ frappe.utils.formatdate(doc.date_of_departure) }}<br>
Time: {{ doc.time_of_departure }}
</p>
