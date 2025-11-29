export default class Tab {
	constructor(layout, df, frm, tab_link_container, tabs_content) {
		this.layout = layout;
		this.df = df || {};
		this.frm = frm;
		this.doctype = this.frm?.doctype ?? this.df.parent;
		this.label = this.df && this.df.label;
		this.tab_link_container = tab_link_container;
		this.tabs_content = tabs_content;
		this.make();
		this.setup_listeners();
		this.refresh();
	}

	make() {
		const id = `${frappe.scrub(this.doctype, "-")}-${this.df.fieldname}`;
		this.tab_link = $(`
			<li class="nav-item">
				<button class="nav-link ${this.df.active ? "active" : ""}" id="${id}-tab"
					data-toggle="tab"
					data-target="#${id}"
					data-fieldname="${this.df.fieldname}"
					type="button"
					role="tab"
					aria-controls="${id}">
						${__(this.label, null, this.doctype)}
				</button>
			</li>
		`).appendTo(this.tab_link_container);

		this.wrapper = $(`<div class="tab-pane fade show ${this.df.active ? "active" : ""}"
			id="${id}" role="tabpanel" aria-labelledby="${id}-tab">`).appendTo(this.tabs_content);
	}

	refresh() {
		if (!this.df) return;

		// hide if explicitly hidden
		let hide = this.df.hidden || this.df.hidden_due_to_dependency;

		// hide if no read permission
		if (!hide && this.frm && !this.frm.get_perm(this.df.permlevel || 0, "read")) {
			hide = true;
		}

		if (!hide) {
			// show only if there is at least one visible section or control
			hide = true;
			const visible_sections = this.wrapper.find(
				".form-section:not(.hide-control, .empty-section), .form-dashboard-section:not(.hide-control, .empty-section)"
			);
			if (visible_sections.length) {
				hide = false;
			}
		}

		this.toggle(!hide);
	}

	toggle(show) {
		this.tab_link.toggleClass("hide", !show);
		this.wrapper.toggleClass("hide", !show);
		this.tab_link.toggleClass("show", show);
		this.wrapper.toggleClass("show", show);
		this.hidden = !show;
	}

	show() {
		this.tab_link.show();
	}

	hide() {
		this.tab_link.hide();
	}

	add_field(fieldobj) {
		fieldobj.tab = this;
	}

	replace_field(fieldobj) {
		fieldobj.tab = this;
	}

	set_active() {
		// Use Bootstrap's tab method to properly activate
		this.tab_link.find(".nav-link").tab("show");

		// Ensure the wrapper has the correct classes
		this.wrapper.addClass("show active");

		this.frm?.set_active_tab?.(this);
	}

	is_active() {
		return this.wrapper.hasClass("active");
	}

	is_hidden() {
		return this.wrapper.hasClass("hide") && this.tab_link.hasClass("hide");
	}

	setup_listeners() {
		this.tab_link.find(".nav-link").on("shown.bs.tab", () => {
			this.frm?.set_active_tab?.(this);
		});

		// For child tables, add explicit click handler to ensure tab switching works
		if (this.layout?.is_child_table) {
			this.tab_link.find(".nav-link").on("click", (e) => {
				e.preventDefault();
				e.stopPropagation();

				// Deactivate all other tabs
				this.layout.tabs.forEach((tab) => {
					if (tab !== this) {
						tab.tab_link.find(".nav-link").removeClass("active");
						tab.wrapper.removeClass("show active");
					}
				});

				// Activate this tab
				this.tab_link.find(".nav-link").addClass("active");
				this.wrapper.addClass("show active");
			});
		}
	}
}
