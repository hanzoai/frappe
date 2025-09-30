// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Desktop Icon", {
	setup: function (frm) {
		load_installed_apps();
		frm.fields_dict.color.set_data(Object.keys(frappe.palette_map));
	},
	before_save: function (frm) {
		if (frm.doc.type == "workspace") {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Workspace", // e.g., "User"
					name: frm.doc.workspace,
				},
				callback: function (r) {
					if (r.message) {
						// Access attributes like r.message.another_field
						let doc = r.message;
						let url = `/app/${
							doc.public
								? frappe.router.slug(doc.title)
								: "private/" + frappe.router.slug(doc.title)
						}`;
						frm.doc.route = url;
					}
				},
			});
		} else if (frm.doc.type == "link") {
			frm.doc.route = frm.doc.link;
		} else if (frm.doc.type == "list") {
			frm.doc.route = `/app/${frappe.router.slug(frm.doc._doctype)}`;
		}
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
