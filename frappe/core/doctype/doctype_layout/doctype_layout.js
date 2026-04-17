// Copyright (c) 2020, Frappe Technologies and contributors
// For license information, please see license.txt

/* ─────────────────────────────────────────────────────────────────────────────
 * DocType Layout – visual layout builder
 *
 * Uses the same Form Builder UI (form_builder.bundle.js) with is_layout=true
 * so the canvas/drag-drop/properties panel reuse the existing infrastructure.
 *  • Drag-and-drop reordering via vuedraggable
 *  • Selected field → properties panel (overrideable props only)
 *  • Per-field overrides: label, hidden, reqd, read_only, bold, allow_in_quick_entry,
 *    in_list_view, in_standard_filter, default, description,
 *    depends_on, mandatory_depends_on, read_only_depends_on
 *  • Adding/removing fields and structural changes are disabled
 *  • "Sync Fields" fetches latest fields from the DocType definition
 * ───────────────────────────────────────────────────────────────────────────── */

frappe.ui.form.on("DocType Layout", {
	// ── lifecycle ──────────────────────────────────────────────────────────────

	onload(frm) {
		// Full-width page so the Form Builder canvas has maximum horizontal space
		frm.page.wrapper.addClass("doctype-layout-full-width");
		if (!document.getElementById("doctype-layout-fw-style")) {
			const style = document.createElement("style");
			style.id = "doctype-layout-fw-style";
			style.textContent = `
				.doctype-layout-full-width .layout-side-section { display: none !important; }
				.doctype-layout-full-width .layout-main-section-wrapper {
					width: 100% !important;
					max-width: 100% !important;
				}
			`;
			document.head.appendChild(style);
		}
	},

	onload_post_render(frm) {
		frm.events.render_builder(frm);
	},

	// Re-render when user switches to the Form tab
	tab_break_form(frm) {
		frm.events.render_builder(frm);
	},

	before_save(frm) {
		let builder = frappe.layout_builder;
		if (builder?.store) {
			let result = builder.store.update_fields();
			if (typeof result === "string") {
				frappe.throw(result);
			}
		}
	},

	after_save(frm) {
		if (frappe.layout_builder?.store) {
			frappe.layout_builder.store.fetch();
		}
	},

	refresh(frm) {
		if (frm.doc.is_standard && !frappe.boot.developer_mode) {
			frm.set_read_only();
			frm.fields
				.filter((f) => f.has_input)
				.forEach((f) => frm.set_df_property(f.df.fieldname, "read_only", "1"));
			frm.disable_save();
		}
		frm.events.add_buttons(frm);
	},

	async document_type(frm) {
		if (frm.doc.document_type) {
			frm.set_value("fields", []);
			await frm.events.sync_fields(frm, false);
			frm.events.render_builder(frm);
		}
	},

	// ── buttons ────────────────────────────────────────────────────────────────

	add_buttons(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Go to {0} List", [frm.doc.title || frm.doc.name]), () => {
				frappe.set_route(frappe.router.slug(frm.doc.name));
			});
		}

		frm.add_custom_button(__("Sync Fields"), async () => {
			await frm.events.sync_fields(frm, true);
			if (frappe.layout_builder?.store) {
				frappe.layout_builder.store.fetch();
			} else {
				frm.events.render_builder(frm);
			}
		});
	},

	// ── sync helper ────────────────────────────────────────────────────────────

	async sync_fields(frm, notify) {
		frappe.dom.freeze(__("Fetching fields…"));
		const response = await frm.call({ doc: frm.doc, method: "sync_fields" });
		frappe.dom.unfreeze();

		if (!response.message) {
			notify && frappe.show_alert({ message: __("No changes to sync"), indicator: "blue" });
			return;
		}

		frm.dirty();
		frm.refresh_field("fields");

		if (notify) {
			const { added, removed } = response.message;
			const rows = (fields) =>
				fields.map((f) => `<li>${(f.label || f.fieldname).bold()}</li>`).join("");
			let msg = "";
			if (added.length) msg += `${__("Added")}:<ul>${rows(added)}</ul>`;
			if (removed.length) msg += `${__("Removed")}:<ul>${rows(removed)}</ul>`;
			if (msg)
				frappe.msgprint({ message: msg, indicator: "green", title: __("Synced Fields") });
		}
	},

	// ── visual builder ─────────────────────────────────────────────────────────

	render_builder(frm) {
		if (!frm.doc.document_type) return;

		const wrapper = $(frm.fields_dict["form_builder"].wrapper).parent().parent().parent().parent();

		// If a builder is already live for this frm, just reload its store
		if (frappe.layout_builder?.store && frappe.layout_builder.frm === frm) {
			frappe.layout_builder.setup_page_actions();
			frappe.layout_builder.store.fetch();
			return;
		}

		// Re-use an existing builder instance (different frm, same page lifecycle)
		if (frappe.layout_builder) {
			frappe.layout_builder.$wrapper = wrapper;
			frappe.layout_builder.frm = frm;
			frappe.layout_builder.page = frm.page;
			frappe.layout_builder.doctype = frm.doc.document_type;
			frappe.layout_builder.is_layout = true;
			frappe.layout_builder.init(true);
			frappe.layout_builder.store.fetch();
			return;
		}

		frappe.require("form_builder.bundle.js").then(() => {
			frappe.layout_builder = new frappe.ui.FormBuilder({
				wrapper: wrapper,
				frm: frm,
				doctype: frm.doc.document_type,
				customize: false,
				is_layout: true,
			});
		});
	},
});
