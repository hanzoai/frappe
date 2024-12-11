// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ui.form.on("Property Setter", {
	validate: function (frm) {
<<<<<<< HEAD
		if (frm.doc.property_type == "Check" && !["0", "1"].includes(frm.doc.value)) {
=======
		if (frm.doc.property_type == "Check" && !in_list(["0", "1"], frm.doc.value)) {
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			frappe.throw(__("Value for a check field can be either 0 or 1"));
		}
	},
});
