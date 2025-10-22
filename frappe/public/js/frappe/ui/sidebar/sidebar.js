import "./sidebar_item";
frappe.ui.Sidebar = class Sidebar {
	constructor() {
		this.make_dom();
		if (!frappe.boot.setup_complete) {
			// no sidebar if setup is not complete
			return;
		}

		// states
		this.edit_mode = false;
		this.sidebar_expanded = false;
		this.all_sidebar_items = frappe.boot.workspace_sidebar_item;
		this.$items = [];
		this.fields_for_dialog = [];
		this.workspace_sidebar_items = [];
		this.new_sidebar_items = [];
		this.$items_container = this.wrapper.find(".sidebar-items");
		this.$sidebar = this.wrapper.find(".body-sidebar");
		this.setup_events();
	}

	prepare() {
		this.workspace_sidebar_items =
			frappe.boot.workspace_sidebar_item[this.workspace_title.toLowerCase()];
		this.choose_app_name();
		this.find_nested_items();
	}
	async fetch_sidebar() {
		const me = this;
		if (me.fields_for_dialog.length > 0) return;
		await frappe.model.with_doctype("Workspace Sidebar Item", () => {
			// get all date and datetime fields
			me.fields_for_dialog = frappe.get_meta("Workspace Sidebar Item").fields;
			let field = me.fields_for_dialog.find((f) => f.label == "Child Item");
			field.hidden = 1;
		});
	}
	choose_app_name() {
		if (frappe.boot.app_name_style == "Default") return;
		frappe.boot.app_data.forEach((a) => {
			if (a.workspaces.includes(frappe.utils.to_title_case(this.workspace_title))) {
				this.app_name = a.app_title;
				this.app_logo_url = a.app_logo_url;
			}
		});
	}

	find_nested_items() {
		const me = this;
		let currentSection = null;
		const updated_items = [];

		this.workspace_sidebar_items.forEach((item) => {
			item.nested_items = [];

			if (item.type === "Section Break") {
				currentSection = item;
				updated_items.push(item);
			} else if (currentSection && item.child) {
				currentSection.nested_items.push(item);
			} else {
				updated_items.push(item);
			}
		});
		this.workspace_sidebar_items = updated_items;
	}
	setup(workspace_title) {
		this.workspace_title = workspace_title;
		this.prepare();
		this.$sidebar.attr("data-title", this.workspace_title);
		this.sidebar_header = new frappe.ui.SidebarHeader(this);
		this.make_sidebar();
		this.setup_complete = true;
	}
	setup_events() {
		const me = this;
		frappe.router.on("change", function (router) {
			frappe.app.sidebar.set_workspace_sidebar();
		});
		$(document).on("page-change", function () {
			frappe.app.sidebar.toggle();
		});
		$(document).on("form-refresh", function () {
			frappe.app.sidebar.toggle();
		});
	}

	toggle() {
		if (!frappe.container.page.page) return;
		if (frappe.container.page.page.hide_sidebar) {
			this.wrapper.hide();
		} else {
			this.wrapper.show();
			this.set_sidebar_for_page();
		}
	}
	make_dom() {
		this.wrapper = $(frappe.render_template("sidebar")).prependTo("body");

		this.$sidebar = this.wrapper.find(".sidebar-items");

		this.wrapper.find(".body-sidebar .collapse-sidebar-link").on("click", () => {
			this.toggle_width();
		});

		this.wrapper.find(".overlay").on("click", () => {
			this.close();
		});
	}

	set_active_workspace_item() {
		if (this.is_route_in_sidebar()) {
			this.active_item.addClass("active-sidebar");
		}
	}

	is_route_in_sidebar() {
		let match = false;
		const that = this;
		$(".item-anchor").each(function () {
			if ($(this).attr("href") == decodeURIComponent(window.location.pathname)) {
				match = true;
				if (that.active_item) that.active_item.removeClass("active-sidebar");
				that.active_item = $(this).parent();
				// this exists the each loop
				return false;
			}
		});
		return match;
	}

	set_sidebar_state() {
		this.sidebar_expanded = true;
		if (localStorage.getItem("sidebar-expanded") !== null) {
			this.sidebar_expanded = JSON.parse(localStorage.getItem("sidebar-expanded"));
		}

		if (frappe.is_mobile()) {
			this.sidebar_expanded = false;
		}

		if (this.workspace_sidebar_items.length === 0) {
			this.sidebar_expanded = true;
		}

		this.expand_sidebar();
	}
	empty() {
		if (this.wrapper.find(".sidebar-items")[0]) {
			this.wrapper.find(".sidebar-items").html("");
		}
	}
	make_sidebar() {
		this.empty();
		this.wrapper.find(".collapse-sidebar-link").removeClass("hidden");
		this.create_sidebar(this.workspace_sidebar_items);

		// Scroll sidebar to selected page if it is not in viewport.
		this.wrapper.find(".selected").length &&
			!frappe.dom.is_element_in_viewport(this.wrapper.find(".selected")) &&
			this.wrapper.find(".selected")[0].scrollIntoView();

		this.set_active_workspace_item();
		this.set_sidebar_state();
	}
	create_sidebar(items) {
		this.empty();
		if (items && items.length > 0) {
			items.forEach((w) => {
				if (!w.display_depends_on || frappe.utils.eval(w.display_depends_on)) {
					this.add_item(w);
				}
			});
		} else {
			let no_items_message = $(
				"<div class='flex' style='padding: 30px'> No Sidebar Items </div>"
			);
			this.wrapper.find(".sidebar-items").append(no_items_message);
			this.wrapper.find(".collapse-sidebar-link").addClass("hidden");
		}
		if (this.edit_mode) {
			$(".edit-menu").removeClass("hidden");
		}
		this.handle_outside_click();
	}

	add_item(item) {
		this.make_sidebar_item({
			container: this.$items_container,
			item: item,
		});
	}
	make_sidebar_item(opts) {
		let class_name = `Type${frappe.utils.to_title_case(opts.item.type).replace(/ /g, "")}`;

		return new frappe.ui.sidebar_item[class_name](opts);
	}
	update_item(item, index) {}

	remove_item(item, index) {}

	toggle_width() {
		if (!this.sidebar_expanded) {
			this.open();
		} else {
			this.close();
		}
	}

	expand_sidebar() {
		let direction;
		if (this.sidebar_expanded) {
			this.wrapper.addClass("expanded");
			// this.sidebar_expanded = false
			direction = "left";
		} else {
			this.wrapper.removeClass("expanded");
			// this.sidebar_expanded = true
			direction = "right";
		}

		localStorage.setItem("sidebar-expanded", this.sidebar_expanded);
		this.wrapper
			.find(".body-sidebar .collapse-sidebar-link")
			.find("use")
			.attr("href", `#icon-arrow-${direction}-to-line`);
		this.sidebar_header.toggle_width(this.sidebar_expanded);
		$(document).trigger("sidebar-expand", {
			sidebar_expand: this.sidebar_expanded,
		});
	}

	close() {
		this.sidebar_expanded = false;

		this.expand_sidebar();
		if (frappe.is_mobile()) frappe.app.sidebar.prevent_scroll();
	}
	open() {
		this.sidebar_expanded = true;
		this.expand_sidebar();
		this.set_active_workspace_item();
	}

	reload() {
		return frappe.workspace.get_pages().then((r) => {
			frappe.boot.sidebar_pages = r;
			this.setup_pages();
		});
	}
	set_height() {
		$(".body-sidebar").css("height", window.innerHeight + "px");
		$(".overlay").css("height", window.innerHeight + "px");
		document.body.style.overflow = "hidden";
	}

	handle_outside_click() {
		document.addEventListener("click", (e) => {
			if (this.sidebar_header.drop_down_expanded) {
				if (!e.composedPath().includes(this.sidebar_header.app_switcher_dropdown)) {
					this.sidebar_header.toggle_dropdown_menu();
				}
			}
		});
	}

	prevent_scroll() {
		let main_section = $(".main-section");
		if (this.sidebar_expanded) {
			main_section.css("overflow", "hidden");
		} else {
			main_section.css("overflow", "");
		}
	}

	set_workspace_sidebar() {
		let route = frappe.get_route();
		if (frappe.get_route()[0] == "setup-wizard") return;
		if (route[0] == "Workspaces") {
			let workspace = route[1] || "Build";
			frappe.app.sidebar.setup(workspace);
		} else if (route[0] == "List" || route[0] == "Form") {
			let doctype = route[1];
			let sidebars = this.get_correct_workspace_sidebars(doctype);
			if (this.workspace_title && sidebars.includes(this.workspace_title.toLowerCase())) {
				frappe.app.sidebar.setup(this.workspace_title.toLowerCase());
			} else {
				frappe.app.sidebar.setup(sidebars[0] || "Build");
			}
		} else if (route[0] == "query-report") {
			let doctype = route[1];
			let sidebars = this.get_correct_workspace_sidebars(doctype);
			if (this.workspace_title && sidebars.includes(this.workspace_title.toLowerCase())) {
				frappe.app.sidebar.setup(this.workspace_title.toLowerCase());
			} else {
				frappe.app.sidebar.setup(sidebars[0] || "Build");
			}
		}

		this.set_active_workspace_item();
	}

	set_sidebar_for_page() {
		let route = frappe.get_route();
		let views = ["List", "Form", "Workspaces", "query-report"];
		let matches = views.some((view) => route.includes(view));
		if (matches) return;
		let workspace_title;
		if (route.length == 2) {
			workspace_title = this.get_correct_workspace_sidebars(route[1]);
		} else {
			workspace_title = this.get_correct_workspace_sidebars(route);
		}
		let module_name = workspace_title ? workspace_title[0] : "Build";
		frappe.app.sidebar.setup(module_name || this.workspace_title || "Build");
	}

	get_correct_workspace_sidebars(link_to) {
		let sidebars = [];
		Object.entries(this.all_sidebar_items).forEach(([name, items]) => {
			items.forEach((item) => {
				if (item.link_to == link_to) {
					sidebars.push(name);
				}
			});
		});
		return sidebars;
	}

	toggle_editing_mode() {
		const me = this;
		this.fetch_sidebar();
		if (this.edit_mode) {
			this.wrapper.attr("data-mode", "edit");
			this.new_sidebar_items = Array.from(me.workspace_sidebar_items);
			$(this.active_item).removeClass("active-sidebar");
			$(".collapse-sidebar-link").hide();
			this.wrapper.find(".edit-mode").removeClass("hidden");
			this.add_new_item_button = this.wrapper.find("[data-name='add-sidebar-item']");
			this.setup_sorting();
			this.setup_editing_controls();
			this.add_new_item_button.on("click", function () {
				me.show_new_dialog();
			});
		} else {
			$(this.active_item).addClass("active-sidebar");
			$(".collapse-sidebar-link").show();
			this.wrapper.find(".edit-mode").addClass("hidden");
			this.add_new_item_button = this.wrapper.find("[data-name='add-sidebar-item']");
		}
	}
	setup_sorting() {
		const me = this;
		this.sortable = Sortable.create($(".sidebar-items").get(0), {
			handler: ".drag-handle",
			onEnd: function (event) {
				if (me.new_sidebar_items.length == 0) {
					me.new_sidebar_items = Array.from(me.workspace_sidebar_items);
				}
				let old_index = event.oldIndex;
				let new_index = event.newIndex;
				me.new_sidebar_items[old_index];
				let b = me.new_sidebar_items[old_index];
				me.new_sidebar_items[old_index] = me.new_sidebar_items[new_index];
				me.new_sidebar_items[new_index] = b;
			},
		});
	}
	make_dialog(item = {}, index) {
		this.fields_for_dialog;
		const fields = this.fields_for_dialog;
		fields.splice(8, 0, {
			fieldtype: "Section Break",
			depends_on: 'eval: doc.type == "Section Break"',
		});
		fields.splice(9, 0, {
			label: "Nested Sidebar Items",
			fieldname: "nested_items",
			fieldtype: "Table",
			fields: this.make_fields_for_grids(fields),
			data: [],
			depends_on: 'eval: doc.type == "Section Break"',
		});
		let title = "New Sidebar Item";
		if (item) {
			if (item.nested_items && item.nested_items.length > 0) {
				fields[-1].data = item.nested_items;
			}
			fields.forEach((f) => {
				if (
					item[f.fieldname] !== undefined &&
					f.fieldtype !== "Section Break" &&
					f.fieldtype !== "Column Break"
				) {
					f.default = item[f.fieldname];
				}
			});
			title = "Edit Sidebar Item";
		}

		const me = this;
		// Create the dialog
		let d = new frappe.ui.Dialog({
			title: title,
			fields: fields,
			primary_action_label: "Save",
			size: "small",
			primary_action(values) {
				if (me.new_sidebar_items.length === 0) {
					me.new_sidebar_items = Array.from(me.workspace_sidebar_items);
				}

				if (typeof index === "number") {
					me.new_sidebar_items.splice(index, 1, values);
				} else {
					if (values.length && values.nested_items.length > 0) {
						let index = me.new_sidebar_items.findIndex((f) => {
							return f.label == values.label;
						});
						me.new_sidebar_items[index].nested_items = values.nested_items;
					} else {
						me.new_sidebar_items.push(values);
					}
				}

				me.create_sidebar(me.new_sidebar_items);
				d.hide();
			},
		});

		return d;
	}

	setup_editing_controls() {
		const me = this;
		this.save_sidebar_button = this.wrapper.find(".save-sidebar");
		this.discard_button = this.wrapper.find(".discard-button");
		this.save_sidebar_button.on("click", async function (event) {
			frappe.show_alert({
				message: __("Saving Sidebar"),
				indicator: "success",
			});
			me.new_sidebar_items = me.new_sidebar_items.map((item, idx) => ({
				...item,
				idx: idx,
			}));
			await frappe.call({
				type: "POST",
				method: "frappe.desk.doctype.workspace_sidebar.workspace_sidebar.add_sidebar_items",
				args: {
					sidebar_title: me.workspace_title,
					sidebar_items: me.new_sidebar_items,
				},
				callback: function (r) {
					frappe.boot.workspace_sidebar_item[me.workspace_title.toLowerCase()] = [
						...me.new_sidebar_items,
					];
					me.edit_mode = false;
					me.toggle_editing_mode();
					me.make_sidebar(me);
				},
			});
		});

		this.discard_button.on("click", function () {
			me.edit_mode = false;
			me.toggle_editing_mode();
			me.make_sidebar(me);
		});
	}

	delete_item(item) {
		let index = this.new_sidebar_items.indexOf(item);
		this.new_sidebar_items.splice(index, 1);
		this.create_sidebar(this.new_sidebar_items);
	}

	add_below(item) {
		let index = this.workspace_sidebar_items.indexOf(item);
		this.show_new_dialog(index);
		this.create_sidebar(this.new_sidebar_items);
	}

	duplicate_item(item) {
		let index = this.workspace_sidebar_items.indexOf(item);
		this.new_sidebar_items.splice(index, 0, item);
		this.create_sidebar(this.new_sidebar_items);
	}

	edit_item(item) {
		let d = this.make_dialog(item);
		d.show();
	}

	show_new_dialog(index) {
		let d = this.make_dialog(index);
		d.show();
	}
	make_fields_for_grids(fields) {
		let doc_fields = Array.from(fields);
		doc_fields = doc_fields
			.filter((f) => f.fieldtype !== "Section Break" && f.fieldtype !== "Column Break")
			.map((f, i) => ({
				...f,
				in_list_view: i < 5 ? 1 : 0,
			}));
		let link_to_field = doc_fields.find((f) => f.label == "Link To");
		link_to_field.field_in_dialog = true;
		return doc_fields;
	}
};
