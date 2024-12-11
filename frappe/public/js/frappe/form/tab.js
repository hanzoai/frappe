export default class Tab {
<<<<<<< HEAD
	constructor(layout, df, frm, tab_link_container, tabs_content) {
		this.layout = layout;
		this.df = df || {};
		this.frm = frm;
		this.doctype = this.frm?.doctype ?? this.df.parent;
		this.label = this.df && this.df.label;
		this.tab_link_container = tab_link_container;
		this.tabs_content = tabs_content;
=======
	constructor(parent, df, frm, tabs_list, tabs_content) {
		this.parent = parent;
		this.df = df || {};
		this.frm = frm;
		this.doctype = this.frm.doctype;
		this.label = this.df && this.df.label;
		this.tabs_list = tabs_list;
		this.tabs_content = tabs_content;
		this.fields_list = [];
		this.fields_dict = {};
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		this.make();
		this.setup_listeners();
		this.refresh();
	}

	make() {
		const id = `${frappe.scrub(this.doctype, "-")}-${this.df.fieldname}`;
<<<<<<< HEAD
		this.tab_link = $(`
			<li class="nav-item">
				<a class="nav-link ${this.df.active ? "active" : ""}" id="${id}-tab"
					data-toggle="tab"
					data-fieldname="${this.df.fieldname}"
					href="#${id}"
					role="tab"
					aria-controls="${id}">
						${__(this.label)}
				</a>
			</li>
		`).appendTo(this.tab_link_container);
=======
		this.parent = $(`
			<li class="nav-item">
				<a class="nav-link ${this.df.active ? "active" : ""}" id="${id}-tab"
					data-toggle="tab"
					href="#${id}"
					role="tab"
					aria-controls="${this.label}">
						${__(this.label)}
				</a>
			</li>
		`).appendTo(this.tabs_list);
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

		this.wrapper = $(`<div class="tab-pane fade show ${this.df.active ? "active" : ""}"
			id="${id}" role="tabpanel" aria-labelledby="${id}-tab">`).appendTo(this.tabs_content);
	}

	refresh() {
		if (!this.df) return;

		// hide if explicitly hidden
		let hide = this.df.hidden || this.df.hidden_due_to_dependency;

<<<<<<< HEAD
=======
		// hide if dashboard and not saved
		if (!hide && this.df.show_dashboard && this.frm.is_new() && !this.fields_list.length) {
			hide = true;
		}

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		// hide if no read permission
		if (!hide && this.frm && !this.frm.get_perm(this.df.permlevel || 0, "read")) {
			hide = true;
		}

		if (!hide) {
			// show only if there is at least one visible section or control
			hide = true;
			if (
				this.wrapper.find(
					".form-section:not(.hide-control, .empty-section), .form-dashboard-section:not(.hide-control, .empty-section)"
				).length
			) {
				hide = false;
			}
		}

		this.toggle(!hide);
	}

	toggle(show) {
<<<<<<< HEAD
		this.tab_link.toggleClass("hide", !show);
		this.wrapper.toggleClass("hide", !show);
		this.tab_link.toggleClass("show", show);
=======
		this.parent.toggleClass("hide", !show);
		this.wrapper.toggleClass("hide", !show);
		this.parent.toggleClass("show", show);
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		this.wrapper.toggleClass("show", show);
		this.hidden = !show;
	}

	show() {
<<<<<<< HEAD
		this.tab_link.show();
	}

	hide() {
		this.tab_link.hide();
	}

	add_field(fieldobj) {
		fieldobj.tab = this;
=======
		this.parent.show();
	}

	hide() {
		this.parent.hide();
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	}
	replace_field(fieldobj) {
		fieldobj.tab = this;
	}

	set_active() {
<<<<<<< HEAD
		this.tab_link.find(".nav-link").tab("show");
=======
		this.parent.find(".nav-link").tab("show");
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		this.wrapper.addClass("show");
		this.frm?.set_active_tab?.(this);
	}

	is_active() {
		return this.wrapper.hasClass("active");
	}

	is_hidden() {
<<<<<<< HEAD
		return this.wrapper.hasClass("hide") && this.tab_link.hasClass("hide");
	}

	setup_listeners() {
		this.tab_link.find(".nav-link").on("shown.bs.tab", () => {
=======
		return this.wrapper.hasClass("hide");
	}

	setup_listeners() {
		this.parent.find(".nav-link").on("shown.bs.tab", () => {
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			this?.frm.set_active_tab?.(this);
		});
	}
}
