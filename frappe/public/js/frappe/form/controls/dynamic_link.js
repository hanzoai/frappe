frappe.ui.form.ControlDynamicLink = class ControlDynamicLink extends frappe.ui.form.ControlLink {
	get_options() {
		let options = "";
		if (this.df.get_options) {
			options = this.df.get_options(this);
		} else if (this.docname == null && cur_dialog) {
			//for dialog box
			options = cur_dialog.get_value(this.df.options);
		} else if (!cur_frm) {
			if (cur_list) {
				// for list page
				options = cur_list.page.fields_dict[this.df.options].get_input_value();
			}
			if (cur_page) {
				options = cur_page.page.fields_dict[this.df.options].get_input_value();
			}
		} else {
			options = frappe.model.get_value(this.df.parent, this.docname, this.df.options);
		}

		if (frappe.model.is_single(options)) {
			frappe.throw(__("{0} is not a valid DocType for Dynamic Link", [options.bold()]));
		}

		return options;
	}
};
