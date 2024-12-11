frappe.listview_settings["Note"] = {
<<<<<<< HEAD
	hide_name_column: true,
	add_fields: ["public"],
=======
	onload: function (me) {
		me.page.set_title(__("Notes"));
	},
	add_fields: ["title", "public"],
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	get_indicator: function (doc) {
		if (doc.public) {
			return [__("Public"), "green", "public,=,Yes"];
		} else {
			return [__("Private"), "gray", "public,=,No"];
		}
	},
};
