// Copyright (c) 2026, bharathiraja and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        // Show button only for saved documents
        if (!frm.is_new()) {
            frm.add_custom_button(
                __("Assign Seat"),
                () => {
                    open_seat_dialog(frm);
                }
            );
        }
    }
});

function open_seat_dialog(frm) {
    let dialog = new frappe.ui.Dialog({
        title: __("Assign Seat"),
        fields: [
            {
                fieldname: "seat",
                label: __("Seat Number"),
                fieldtype: "Data",
                reqd: 1,
                description: "Example: 12A, 45C"
            }
        ],
        primary_action_label: __("Assign"),
        primary_action(values) {
            frm.set_value("seat", values.seat);
            dialog.hide();
        }
    });

    dialog.show();
}
