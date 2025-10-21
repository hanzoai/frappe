frappe.provide("frappe.ui.sidebar_item");
frappe.ui.sidebar_item.TypeLink = class SidebarItem {
	constructor(opts) {
		this.item = opts.item;
		this.container = opts.container;
		this.nested_items = opts.item.nested_items || [];
		this.workspace_title = $(".body-sidebar").attr("data-title").toLowerCase();
		this.prepare(opts);
		this.make();
	}
	get_path() {
		let path;
		if (this.item.type === "Link") {
			if (this.item.link_type === "Report") {
				let args = {
					type: this.item.link_type,
					name: this.item.link_to,
					is_query_report:
						this.item.report.report_type === "Query Report" ||
						this.item.report.report_type == "Script Report",
					report_ref_doctype: this.item.report.ref_doctype,
				};
				if (!this.item.report) {
					delete args.is_query_report;
				}
				path = frappe.utils.generate_route(args);
			} else if (this.item.link_type == "Workspace") {
				path = "/app/" + frappe.router.slug(this.item.link_to);
				if (this.item.route) {
					path = this.item.route;
				}
			} else {
				path = frappe.utils.generate_route({
					type: this.item.link_type,
					name: this.item.link_to,
				});
			}
		} else if (this.item.type === "URL") {
			path = this.item.external_link;
		}
		return path;
	}
	prepare() {}
	make() {
		this.path = this.get_path();
		this.wrapper = $(
			frappe.render_template("sidebar_item", {
				item: this.item,
				path: this.path,
				edit_mode: frappe.app.sidebar.edit_mode,
			})
		);
		this.setup_editing_controls();
		$(this.container).append(this.wrapper);
	}
	setup_editing_controls() {
		let me = this;
		let menu_items = [
			{
				label: "Edit Item",
				icon: "pen",
				onClick: () => {
					console.log("Start ediitng");
					frappe.app.sidebar.edit_item(me.item);
				},
			},
			{
				label: "Add Item Below",
				icon: "add",
				onClick: () => {
					frappe.app.sidebar.add_below(me.item);
				},
			},
			{
				label: "Duplicate",
				icon: "copy",
				onClick: () => {
					console.log("Start Deleting");
					frappe.app.sidebar.duplicate_item(me.item);
				},
			},
			{
				label: "Delete",
				icon: "trash-2",
				onClick: () => {
					console.log(me.item);
					frappe.app.sidebar.delete_item(me.item);
					console.log("Start Deleting");
				},
			},
		];
		this.menu = new frappe.ui.menu(menu_items);
		this.$edit_menu = this.wrapper.find(".edit-menu");
		this.$sidebar_container = this.$edit_menu.parent();
		frappe.ui.create_menu(this.$edit_menu, menu_items);
	}
};

frappe.ui.sidebar_item.TypeSectionBreak = class SectionBreakSidebarItem extends (
	frappe.ui.sidebar_item.TypeLink
) {
	prepare(opts) {
		this.collapsed = false;
		this.nested_items = opts.item.nested_items || this.nested_items;
		this.items = [];
		this.$items = [];
		const storedState = localStorage.getItem("section-breaks-state");
		this.section_breaks_state = storedState ? JSON.parse(storedState) : {};
	}
	add_items() {
		this.$item_control = this.wrapper.find(".sidebar-item-control");
		this.$nested_items = this.wrapper.find(".nested-container").first();
		this.nested_items.forEach((f) => {
			frappe.app.sidebar.make_sidebar_item({
				container: this.$nested_items,
				item: f,
			});
		});
		this.full_template = $(this.wrapper);
	}
	make() {
		super.make();
		this.add_items();
		this.toggle_on_collapse();
		this.enable_collapsible(this.item, this.full_template);
		$(this.container).append(this.full_template);
	}

	setup_events() {
		const me = this;
	}
	open() {
		this.collapsed = false;
		this.toggle();
	}
	close() {
		this.collapsed = true;
		this.toggle();
	}
	toggle() {
		if (!this.collapsed) {
			this.$drop_icon
				.attr("data-state", "closed")
				.find("use")
				.attr("href", "#icon-chevron-down");
		} else {
			this.$drop_icon
				.attr("data-state", "opened")
				.find("use")
				.attr("href", "#icon-chevron-right");
		}

		$(this.$nested_items).toggleClass("hidden");
	}
	toggle_on_collapse() {
		const me = this;
		$(document).on("sidebar-expand", function (event, expand) {
			if (expand.sidebar_expand) {
				$(me.wrapper.find(".section-break")).removeClass("hidden");
				$(me.wrapper.find(".divider")).addClass("hidden");
			} else {
				$(me.wrapper.find(".section-break")).addClass("hidden");
				$(me.wrapper.find(".divider")).removeClass("hidden");
			}
		});
	}

	enable_collapsible(item, $item_container) {
		let sidebar_control = this.$item_control;
		let drop_icon = "chevron-down";
		if (item.collapsible) {
			this.$drop_icon = $(`<button class="btn-reset drop-icon hidden">`)
				.html(frappe.utils.icon(drop_icon, "sm"))
				.appendTo(sidebar_control);

			this.$drop_icon.removeClass("hidden");
			this.setup_event_listner($item_container);
		}

		if (item.keep_closed) {
			this.close();
		}
		if (
			Object.keys(this.section_breaks_state) &&
			this.section_breaks_state[this.workspace_title]
		) {
			this.apply_section_break_state();
		}
	}
	apply_section_break_state() {
		const me = this;
		let current_sidebar_state = this.section_breaks_state[this.workspace_title];
		for (const [element_name, collapsed] of Object.entries(current_sidebar_state)) {
			if ($(this.wrapper).attr("item-name") == element_name) {
				if (collapsed) {
					me.close();
				} else {
					me.open();
				}
			}
		}
	}
	setup_event_listner() {
		const me = this;
		let $child_item_section = $(this.$nested_items);

		this.$drop_icon.on("click", (e) => {
			me.collapsed = me.$drop_icon.find("use").attr("href") === "#icon-chevron-down";
			me.toggle();

			if (e.originalEvent.isTrusted) {
				me.save_section_break_state();
			}
		});
	}
	save_section_break_state() {
		if (Object.keys(this.section_breaks_state).length == 0) {
			this.section_breaks_state[this.workspace_title] = {};
		}

		const title = this.$drop_icon.parent().parent().attr("title");

		this.section_breaks_state[this.workspace_title][title] = this.collapsed;

		localStorage.setItem("section-breaks-state", JSON.stringify(this.section_breaks_state));
	}
};

frappe.ui.sidebar_item.TypeSpacer = class SpacerItem extends frappe.ui.sidebar_item.TypeLink {
	constructor(item, items) {
		super(item);
		delete this.route;
	}
};
