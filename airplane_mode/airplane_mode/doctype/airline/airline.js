// Copyright (c) 2026, bharathiraja and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airline", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airline", {
    refresh(frm) {
        // Remove old link to avoid duplicates
        frm.page.clear_custom_actions();

        // Add link only if website is present
        if (frm.doc.website) {
            frm.add_web_link(
                frm.doc.website,
                __("Official Website")
            );
        }
    }
});
