export class DropdownConsole {
	constructor() {
		this.dialog = new frappe.ui.Dialog({
			title: __("System Console"),
			minimizable: true,
			size: "large",
			fields: [
				{
					description: "To execute press ctrl/cmd+enter.",
					fieldname: "console",
					fieldtype: "Code",
					label: "Console",
					options: "Python",
					min_lines: 20,
					max_lines: 20,
				},
				{
					fieldname: "output",
					fieldtype: "Code",
					label: "Output",
					read_only: 1,
				},
			],
		});
	}

	show() {
		this.dialog.show();
		if (cur_frm && !cur_frm.is_new()) {
			let current_code = this.dialog.get_value("console");
			if (!current_code) {
				this.dialog.set_value(
					"console",
					`doc = frappe.get_doc("${cur_frm.doc.doctype}", "${cur_frm.doc.name}")\n`
				);
			}
		}
	}
}
