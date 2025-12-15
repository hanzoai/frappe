// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt
import ListFilter from "./list_filter";
frappe.provide("frappe.views");

// opts:
// stats = list of fields
// doctype
// parent

frappe.views.ListSidebar = class ListSidebar {
	constructor(opts) {
		$.extend(this, opts);
		this.make();
	}

	make() {
		var sidebar_content = frappe.render_template("list_sidebar", { doctype: this.doctype });

		this.sidebar = $('<div class="list-sidebar overlay-sidebar hidden-xs hidden-sm"></div>')
			.html(sidebar_content)
			.appendTo(this.page.sidebar.empty());

		this.setup_list_filter();
		this.setup_list_group_by();
		this.setup_collapsible();

		// do not remove
		// used to trigger custom scripts
		$(document).trigger("list_sidebar_setup");

		if (
			this.list_view.list_view_settings &&
			this.list_view.list_view_settings.disable_sidebar_stats
		) {
			this.sidebar.find(".list-tags").remove();
		} else {
			this.sidebar.find(".list-stats").on("show.bs.dropdown", (e) => {
				this.reload_stats();
			});
		}
	}

	setup_views() {
		var show_list_link = false;

		if (frappe.views.calendar[this.doctype]) {
			this.sidebar.find('.list-link[data-view="Calendar"]').removeClass("hide");
			this.sidebar.find('.list-link[data-view="Gantt"]').removeClass("hide");
			show_list_link = true;
		}
		//show link for kanban view
		this.sidebar.find('.list-link[data-view="Kanban"]').removeClass("hide");
		if (this.doctype === "Communication" && frappe.boot.email_accounts.length) {
			this.sidebar.find('.list-link[data-view="Inbox"]').removeClass("hide");
			show_list_link = true;
		}

		if (frappe.treeview_settings[this.doctype] || frappe.get_meta(this.doctype).is_tree) {
			this.sidebar.find(".tree-link").removeClass("hide");
		}

		this.current_view = "List";
		var route = frappe.get_route();
		if (route.length > 2 && frappe.views.view_modes.includes(route[2])) {
			this.current_view = route[2];

			if (this.current_view === "Kanban") {
				this.kanban_board = route[3];
			} else if (this.current_view === "Inbox") {
				this.email_account = route[3];
			}
		}

		// disable link for current view
		this.sidebar
			.find('.list-link[data-view="' + this.current_view + '"] a')
			.attr("disabled", "disabled")
			.addClass("disabled");

		//enable link for Kanban view
		this.sidebar
			.find('.list-link[data-view="Kanban"] a, .list-link[data-view="Inbox"] a')
			.attr("disabled", null)
			.removeClass("disabled");

		// show image link if image_view
		if (this.list_view.meta.image_field) {
			this.sidebar.find('.list-link[data-view="Image"]').removeClass("hide");
			show_list_link = true;
		}

		if (
			this.list_view.settings.get_coords_method ||
			(this.list_view.meta.fields.find((i) => i.fieldname === "latitude") &&
				this.list_view.meta.fields.find((i) => i.fieldname === "longitude")) ||
			this.list_view.meta.fields.find(
				(i) => i.fieldname === "location" && i.fieldtype == "Geolocation"
			)
		) {
			this.sidebar.find('.list-link[data-view="Map"]').removeClass("hide");
			show_list_link = true;
		}

		if (show_list_link) {
			this.sidebar.find('.list-link[data-view="List"]').removeClass("hide");
		}
	}

	setup_list_filter() {
		this.list_filter = new ListFilter({
			wrapper: this.page.sidebar.find(".list-filters"),
			doctype: this.doctype,
			list_view: this.list_view,
			section_title: this.page.sidebar.find(".save-filter-section .sidebar-label"),
		});
	}

	setup_collapsible() {
		// tags and save filter sections should be collapsible
		let sections = [
			["tags-section", "list-tags"],
			["save-filter-section", "list-filters"],
			["filter-section", "list-group-by"],
		];

		for (let s of sections) {
			this.page.sidebar.find(`.${s[0]} .sidebar-label`).on("click", () => {
				let list_tags = this.page.sidebar.find("." + s[1]);
				let icon = "#es-line-down";
				list_tags.toggleClass("hide");
				if (list_tags.hasClass("hide")) {
					icon = "#es-line-right-chevron";
				}
				this.page.sidebar.find(`.${s[0]} .es-line use`).attr("href", icon);
			});
		}
	}

	setup_kanban_boards() {
		const $dropdown = this.page.sidebar.find(".kanban-dropdown");
		frappe.views.KanbanView.setup_dropdown_in_sidebar(this.doctype, $dropdown);
	}

	setup_list_group_by() {
		this.list_group_by = new frappe.views.ListGroupBy({
			doctype: this.doctype,
			sidebar: this,
			list_view: this.list_view,
			page: this.page,
		});
	}
};
