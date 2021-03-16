// Copyright (c) 2021, eneegy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Facilities', {
	refresh: function(frm) {
		$("input[data-fieldname|='facility_icon']").iconpicker("input[data-fieldname|='facility_icon']");
	}
});
