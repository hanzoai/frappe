// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Desktop Icon", {
	setup: function (frm) {
		load_installed_apps();
	},
});

async function load_installed_apps(frm) {
	await frappe.call({
		method: "frappe.desk.desktop.get_installed_apps",
		callback: function (r) {
			if (r.message) {
				cur_frm.fields_dict["app"].set_data(r.message);
			}
		},
	});
}
