frappe.ui.form.ControlHeading = class ControlHeading extends frappe.ui.form.ControlHTML {
	get_content() {
<<<<<<< HEAD
		return "<h4>" + __(this.df.label, null, this.df.parent) + "</h4>";
=======
		return "<h4>" + __(this.df.label) + "</h4>";
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	}
};
