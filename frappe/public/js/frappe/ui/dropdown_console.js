export class DropdownConsole {
	constructor() {
		this.dialog = new frappe.ui.Dialog({
			title: __("System Console"),
			minimizable: true,
			no_cancel_flag: true, // ugh
			size: "large",
			fields: [
				{
					description: `To execute press ctrl/cmd+enter.
					To minimize this window press Escape.
					Press shift+t to bring it back.
					`,
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

		// Make it static and avoid closing on escape.
		// Not using dialog.static here because then it's not dismissable at all.
		this.dialog.$wrapper.modal({
			backdrop: "static",
			keyboard: false,
		});

		let me = this;
		this.dialog.$wrapper.on("keydown", function (e) {
			if (e.key === "Escape") {
				e.preventDefault();
				if (!me.dialog.is_minimized) {
					me.dialog.toggle_minimize();
				}
				return false;
			}
		});
	}

	async sleep(duration) {
		// because ace will be ace, this is needed to keep interaction between ace and rest of the
		// code feel saner.
		await new Promise((r) => setTimeout(r, duration));
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

		this.bind_executer();
		this.load_completions();
	}

	async bind_executer() {
		let me = this;
		await this.sleep(200);
		const field = this.dialog.get_field("console");
		let editor = field.editor;
		editor.setKeyboardHandler(null); // sorry emacs/vim users
		editor.commands.addCommand({
			name: "execute_code",
			bindKey: {
				// Shortcut keys
				win: "Ctrl-Enter",
				mac: "Command-Enter",
			},
			exec: function (editor) {
				me.execute_code();
			},
		});
	}

	async execute_code() {
		this.dialog.set_value("output", "");
		let { output } = await frappe.xcall(
			"frappe.desk.doctype.system_console.system_console.execute_code",
			{
				doc: {
					console: this.dialog.get_value("console"),
					doctype: "System Console",
					type: "Python",
				},
			}
		);
		this.dialog.set_value("output", output);
	}

	async load_completions() {
		let me = this;
		await this.sleep(100);
		let items = await frappe.xcall(
			"frappe.core.doctype.server_script.server_script.get_autocompletion_items",
			null,
			"GET",
			{ cache: true }
		);
		const field = me.dialog.get_field("console");
		const custom_completions = [];
		if (cur_frm && !cur_frm.is_new()) {
			frappe.meta
				.get_fieldnames(cur_frm.doc.doctype, cur_frm.doc.parent, {
					fieldtype: ["not in", frappe.model.no_value_type],
				})
				.forEach((fieldname) => {
					custom_completions.push(`doc.${fieldname}`);
				});
		}

		field.df.autocompletions = [...items, ...custom_completions];
	}
}
