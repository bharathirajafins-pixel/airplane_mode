
frappe.ready(function () {
    const params = new URLSearchParams(window.location.search);

    const flight = params.get("flight");
    const price = params.get("price");

    console.log("Flight:", flight, "Price:", price);

    if (flight) {
        frappe.web_form.set_value("flight", flight);
    }

    if (price) {
        frappe.web_form.set_value("flight_price", price);
    }
});
