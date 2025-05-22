export class DropdownConsole {
	constructor() {
		this.dialog = new frappe.ui.Dialog({
			title: __("System Console"),
			minimizable: true,
			no_cancel_flag: true, // ugh
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
		this.load_completion();
	}

	bind_executer() {
		let me = this;
		setTimeout(() => {
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
		}, 200); // XXX: figure out a way to chain with readiness of ace?
	}

	async execute_code() {
		this.dialog.set_value("output", "");
		frappe
			.xcall("frappe.desk.doctype.system_console.system_console.execute_code", {
				doc: {
					console: this.dialog.get_value("console"),
					doctype: "System Console",
					type: "Python",
				},
			})
			.then(({ output }) => {
				this.dialog.set_value("output", output);
			});
	}

	async load_completion() {
		let me = this;
		setTimeout(() => {
			frappe
				.xcall(
					"frappe.core.doctype.server_script.server_script.get_autocompletion_items",
					null,
					"GET",
					{ cache: true }
				)
				.then((items) => {
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
				});
		}, 100);
	}
}
