frappe.ui.Sidebar = class Sidebar {
	constructor() {
		this.section_breaks = [];
		this.section_breaks_content = [];
		this.sidebar_expanded = false;
		this.workspace_sidebar_items = [];
		this.closed_section_breaks = {};
		if (!frappe.boot.setup_complete) {
			// no sidebar if setup is not complete
			return;
		}
		this.make_dom();
		this.set_all_pages();
		this.sidebar_items = {
			public: {},
			private: {},
		};
		this.indicator_colors = [
			"green",
			"cyan",
			"blue",
			"orange",
			"yellow",
			"gray",
			"grey",
			"red",
			"pink",
			"darkgrey",
			"purple",
			"light-blue",
		];
		this.setup_pages();
		this.hide_sidebar = false;
		this.setup_events();
	}

	setup(workspace_title) {
		this.workspace_title = workspace_title;
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
			this.toggle_sidebar();
		});

		this.wrapper.find(".overlay").on("click", () => {
			this.close_sidebar();
		});
	}

	set_hover() {
		$(".standard-sidebar-item > .item-anchor:not(.section-break)").on(
			"mouseover",
			function (event) {
				if ($(this).parent().hasClass("active-sidebar")) return;
				$(this).parent().addClass("hover");
			}
		);

		$(".standard-sidebar-item > .item-anchor:not(.section-break)").on(
			"mouseleave",
			function () {
				$(this).parent().removeClass("hover");
			}
		);
	}

	set_all_pages() {
		this.sidebar_items = frappe.boot.workspace_sidebar_item;
	}

	set_default_app() {
		// sort apps based on # of workspaces
		frappe.boot.app_data.sort((a, b) => (a.workspaces.length < b.workspaces.length ? 1 : -1));
		frappe.current_app = frappe.boot.app_data[0].app_name;
		frappe.frappe_toolbar.set_app_logo(frappe.boot.app_data[0].app_logo_url);
	}

	set_active_workspace_item() {
		if (this.is_route_in_sidebar()) {
			this.active_item.addClass("active-sidebar");
		}
	}
	toggle_section_break() {
		this.section_breaks.forEach((f, i) => {
			$(f[0]).html("");
			if (this.sidebar_expanded) {
				$(f[0]).html(this.section_breaks_content[i]);
				this.setup_event_listner($($(f[0]).parent()));
			} else {
				$(f[0]).html("<div class='divider'></div>");
			}
		});
	}

	open_all_section_breaks() {
		this.section_breaks.forEach((f) => {
			const $container = $(f[0]).parent().find(".nested-container");
			const isHidden = $($container[0]).hasClass("hidden");
			const parent = $($(f[0]).children()[0]);

			if (isHidden) {
				$(f[0]).find(".drop-icon").get(0).click();
			}
		});
	}

	open_or_close_section_breaks() {
		if (!this.sidebar_expanded) return;
		this.closed_section_breaks[this.workspace_title]?.forEach((title) => {
			const $section = this.wrapper.find(
				`.sidebar-item-container.section-item[item-title="${title}"]`
			);
			if ($section.length) {
				const $container = $section.find(".nested-container");
				if (!$($container[0]).hasClass("hidden")) {
					$section.find(".drop-icon").get(0).click();
				}
			}
		});
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

	setup_pages() {
		this.set_all_pages();
		if (this.all_pages) {
			frappe.workspaces = {};
			frappe.workspace_list = [];
			frappe.workspace_map = {};
			for (let page of this.all_pages) {
				frappe.workspaces[frappe.router.slug(page.name)] = {
					name: page.name,
					public: page.public,
				};
				if (!page.app && page.module) {
					page.app = frappe.boot.module_app[frappe.slug(page.module)];
				}
				frappe.workspace_map[page.name] = page;
				frappe.workspace_list.push(page);
			}
			this.make_sidebar();
		}
		// this.set_hover();
		// this.set_sidebar_state();
	}
	set_sidebar_state() {
		this.sidebar_expanded = true;
		if (localStorage.getItem("sidebar-expanded") !== null) {
			this.sidebar_expanded = JSON.parse(localStorage.getItem("sidebar-expanded"));
		}
		if (localStorage.getItem("closed-section-breaks") !== null) {
			this.closed_section_breaks = JSON.parse(localStorage.getItem("closed-section-breaks"));
		}
		if (frappe.is_mobile()) {
			this.sidebar_expanded = false;
		}
		this.expand_sidebar();
		this.sidebar_header;
	}
	make_sidebar() {
		if (this.wrapper.find(".sidebar-items")[0]) {
			this.wrapper.find(".sidebar-items").html("");
		}
		this.workspace_sidebar_items =
			frappe.boot.workspace_sidebar_item[this.workspace_title.toLowerCase()];
		// this.build_sidebar_section("All", parent_pages);
		this.create_sidebar();

		// Scroll sidebar to selected page if it is not in viewport.
		this.wrapper.find(".selected").length &&
			!frappe.dom.is_element_in_viewport(this.wrapper.find(".selected")) &&
			this.wrapper.find(".selected")[0].scrollIntoView();

		this.setup_sorting();
		this.set_active_workspace_item();
		this.set_hover();
		this.set_sidebar_state();
	}
	create_sidebar() {
		if (this.workspace_sidebar_items && this.workspace_sidebar_items.length > 0) {
			let parent_links = this.workspace_sidebar_items.filter((f) => f.child !== 1);
			parent_links.forEach((w) => {
				this.append_item(w, this.wrapper.find(".sidebar-items"));
			});
		} else {
			let no_items_message = $(
				"<div class='flex' style='padding: 30px'> No Sidebar Items </div>"
			);
			this.wrapper.find(".sidebar-items").append(no_items_message);
		}
	}
	build_sidebar_section(title, root_pages) {
		let sidebar_section = $(
			`<div class="standard-sidebar-section nested-container" data-title="${title}"></div>`
		);

		this.prepare_sidebar(root_pages, sidebar_section, this.wrapper.find(".sidebar-items"));

		if (Object.keys(root_pages).length === 0) {
			sidebar_section.addClass("hidden");
		}

		$(".item-anchor").on("click", () => {
			$(".list-sidebar.hidden-xs.hidden-sm").removeClass("opened");
			// $(".close-sidebar").css("display", "none");
			$("body").css("overflow", "auto");
			if (frappe.is_mobile()) {
				this.close_sidebar();
			}
		});

		if (
			sidebar_section.find(".sidebar-item-container").length &&
			sidebar_section.find("> [item-is-hidden='0']").length == 0
		) {
			sidebar_section.addClass("hidden show-in-edit-mode");
		}
	}

	prepare_sidebar(items, child_container, item_container) {
		let last_item = null;
		for (let item of items) {
			if (item.public && last_item && !last_item.public) {
				$(`<div class="divider"></div>`).appendTo(child_container);
			}

			// visibility not explicitly set to 0
			if (item.child !== 0) {
				this.append_item(item, child_container);
			}
			last_item = item;
		}
		child_container.appendTo(item_container);
	}

	toggle_sidebar() {
		if (!this.sidebar_expanded) {
			this.open_sidebar();
		} else {
			this.close_sidebar();
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
		this.open_all_section_breaks();
		this.toggle_section_break();
		this.open_or_close_section_breaks();

		this.sidebar_header.toggle_width(this.sidebar_expanded);
	}

	append_item(item, container) {
		let is_current_page = false;

		item.selected = is_current_page;

		if (is_current_page) {
			this.current_page = { name: item.name, public: item.public };
		}

		let $item_container = this.sidebar_item_container(item);
		let sidebar_control = $item_container.find(".sidebar-item-control");

		if (item.type == "Section Break") {
			let current_index = this.workspace_sidebar_items.indexOf(item);
			let sidebar_items = this.workspace_sidebar_items.slice(current_index + 1);
			let next_section_break = sidebar_items.findIndex((f) => f.type == "Section Break");
			let child_items;
			if (next_section_break == -1) {
				child_items = sidebar_items;
			} else {
				child_items = sidebar_items.slice(0, next_section_break);
			}
			if (child_items.length > 0) {
				let child_container = $item_container.find(".sidebar-child-item");
				child_container.addClass("hidden");
				this.prepare_sidebar(child_items, child_container, $item_container);
				this.section_breaks.push($item_container.find(".standard-sidebar-item"));

				$item_container.find(".drop-icon").first().addClass("show-in-edit-mode");
				this.add_toggle_children(item, sidebar_control, $item_container);
				this.section_breaks_content.push(
					$($item_container.find(".standard-sidebar-item")[0]).html()
				);
			}
		}

		$item_container.appendTo(container);
		// this.sidebar_items[item.public ? "public" : "private"][item.name] = $item_container;
	}

	sidebar_item_container(item) {
		item.indicator_color =
			item.indicator_color || this.indicator_colors[Math.floor(Math.random() * 12)];
		let path;
		if (item.type === "Link") {
			if (item.link_type === "Report") {
				path = frappe.utils.generate_route({
					type: item.link_type,
					name: item.link_to,
					is_query_report:
						item.report.report_type === "Query Report" ||
						item.report.report_type == "Script Report",
					report_ref_doctype: item.report.ref_doctype,
				});
			} else if (item.link_type == "Workspace") {
				let label = item.label;
				if (label == "Home") label = this.workspace_title.toLowerCase();
				path = "/app/" + frappe.router.slug(label);
				if (item.route) {
					path = item.route;
				}
			} else {
				path = frappe.utils.generate_route({ type: item.link_type, name: item.link_to });
			}
		} else if (item.type === "URL") {
			path = item.external_link;
		}
		return $(
			frappe.render_template("sidebar_item", {
				item: item,
				path: path,
			})
		);
	}

	add_toggle_children(item, sidebar_control, item_container) {
		let $child_item_section = item_container.find(".sidebar-child-item");
		let drop_icon = "chevron-right";
		if ($child_item_section.children() > 0) {
			drop_icon = "small-up";
		}
		let $drop_icon = $(`<button class="btn-reset drop-icon hidden">`)
			.html(frappe.utils.icon(drop_icon, "sm"))
			.appendTo(sidebar_control);

		if (item.type == "Section Break") {
			$drop_icon.removeClass("hidden");
		}
		this.setup_event_listner(item_container);
	}
	setup_event_listner(item_container) {
		const me = this;
		let $child_item_section = item_container.find(".sidebar-child-item");
		let $drop_icon = item_container.find(".drop-icon");
		$drop_icon.on("click", (e) => {
			let opened = $drop_icon.find("use").attr("href") === "#icon-chevron-down";

			if (!opened) {
				$drop_icon
					.attr("data-state", "closed")
					.find("use")
					.attr("href", "#icon-chevron-down");
			} else {
				$drop_icon
					.attr("data-state", "opened")
					.find("use")
					.attr("href", "#icon-chevron-right");
			}
			$child_item_section.toggleClass("hidden");

			if (e.originalEvent.isTrusted) {
				if (opened) {
					this.closed_section_breaks[me.workspace_title] = [];
				} else {
					const title = $drop_icon.parent().siblings().attr("title");
					// Initialize the array if it doesn't exist
					if (!this.closed_section_breaks[me.workspace_title]) {
						this.closed_section_breaks[me.workspace_title] = [];
					}

					// Push the new title into the array
					this.closed_section_breaks[me.workspace_title].push(title);
				}
				localStorage.setItem(
					"closed-section-breaks",
					JSON.stringify(this.closed_section_breaks)
				);
			}
		});
	}
	toggle_sorting() {
		this.sorting_items.forEach((item) => {
			var state = item.option("disabled");
			item.option("disabled", !state);
		});
	}
	setup_sorting() {
		if (!this.has_access) return;
		this.sorting_items = [];
		for (let container of this.$sidebar.find(".nested-container")) {
			this.sorting_items[this.sorting_items.length] = Sortable.create(container, {
				group: "sidebar-items",
				disabled: true,
				onEnd: () => {
					let sidebar_items = [];
					for (let container of this.$sidebar.find(".nested-container")) {
						for (let item of $(container).children()) {
							let parent = "";
							if ($(item).parent().hasClass("sidebar-child-item")) {
								parent = $(item)
									.parent()
									.closest(".sidebar-item-container")
									.attr("item-name");
							}

							sidebar_items.push({
								name: item.getAttribute("item-name"),
								parent: parent,
							});
						}
					}
					frappe.xcall(
						"frappe.desk.doctype.workspace_settings.workspace_settings.set_sequence",
						{
							sidebar_items: sidebar_items,
						}
					);
				},
			});
		}
	}

	close_sidebar() {
		this.sidebar_expanded = false;

		this.expand_sidebar();
		if (frappe.is_mobile()) frappe.app.sidebar.prevent_scroll();
	}
	open_sidebar() {
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
		let workspace_title;
		let route = frappe.get_route();
		if (frappe.get_route()[0] == "setup-wizard") return;
		let module_name;
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
		Object.entries(this.sidebar_items).forEach(([name, items]) => {
			items.forEach((item) => {
				if (item.link_to == link_to) {
					sidebars.push(name);
				}
			});
		});
		return sidebars;
	}
};
