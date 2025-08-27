frappe.ui.SidebarHeader = class SidebarHeader {
	constructor(sidebar, workspace_title) {
		this.sidebar = sidebar;
		this.sidebar_wrapper = $(".body-sidebar");
		this.drop_down_expanded = false;
		this.workspace_title = workspace_title;
		const me = this;
		this.dropdown_items = [
			{
				name: "desktop",
				label: __("Desktop"),
				icon: "layout-grid",
				onClick: function (el) {
					frappe.set_route("desktop");
				},
			},
			{
				name: "edit-sidebar",
				label: __("Edit Sidebar"),
				icon: "edit",
				onClick: function () {
					if (
						Object.keys(frappe.boot.workspace_sidebar_item).includes(
							me.workspace_title.toLowerCase()
						)
					) {
						frappe.set_route("Form", "Workspace Sidebar", me.workspace_title);
					} else {
						frappe.set_route("List", "Workspace Sidebar");
					}
				},
			},
			{
				name: "website",
				label: __("Website"),
				route: "/",
				icon_url: "/assets/frappe/images/web.svg",
			},
		];
		this.make();
		this.setup_app_switcher();
		this.populate_apps_menu();
		this.setup_select_options();
	}

	make() {
		$(
			frappe.render_template("sidebar_header", {
				workspace_title: this.workspace_title,
			})
		).prependTo(this.sidebar_wrapper);
		this.wrapper = $(".sidebar-header");
		this.dropdown_menu = this.wrapper.find(".sidebar-header-menu");
		this.$header_title = this.wrapper.find(".header-title");
		this.$drop_icon = this.wrapper.find(".drop-icon");
	}

	setup_app_switcher() {
		this.dropdown_menu = $(".sidebar-header-menu");
		$(".sidebar-header").on("click", (e) => {
			this.toggle_app_menu();
			e.stopImmediatePropagation();
		});
	}

	toggle_app_menu() {
		this.toggle_active();
		this.dropdown_menu.toggleClass("hidden");
	}

	populate_apps_menu() {
		const me = this;
		this.dropdown_items.forEach((d) => {
			me.add_app_item(d);
		});
	}

	add_app_item(item) {
		$(`<div class="dropdown-menu-item" data-name="${item.name}"
			data-app-route="${item.route}">
			<a>
				<div class="sidebar-item-icon">
					${
						item.icon
							? frappe.utils.icon(item.icon)
							: `<img
							class="app-logo"
							src="${item.icon_url}"
						>`
					}
				</div>
				<span class="menu-item-title">${item.label}</span>
			</a>
		</div>`).appendTo(this.dropdown_menu);
	}

	setup_select_options() {
		this.dropdown_menu.find(".dropdown-menu-item").on("click", (e) => {
			let item = $(e.delegateTarget);
			let name = item.attr("data-name");
			let current_item = this.dropdown_items.find((f) => f.name == name);
			this.dropdown_menu.toggleClass("hidden");
			this.toggle_active();
			if (current_item.route) [window.open(current_item.route)];
			current_item.onClick(item);
		});
	}

	toggle_active() {
		this.toggle_dropdown();
		this.wrapper.toggleClass("active-sidebar");
		if (!this.sidebar.sidebar_expanded) {
			this.wrapper.removeClass("active-sidebar");
		}
	}

	toggle_dropdown() {
		if (this.drop_down_expanded) {
			this.drop_down_expanded = false;
		} else {
			this.drop_down_expanded = true;
		}
	}

	setup_hover() {
		$(".sidebar-header").on("mouseover", function (event) {
			if ($(this).parent().hasClass("active-sidebar")) return;
			$(this).addClass("hover");
		});

		$(".sidebar-header").on("mouseleave", function () {
			$(this).removeClass("hover");
		});
	}

	toggle_width(expand) {
		let class_name = "collapse-header";
		if (!expand) {
			$(this.wrapper[0]).css("width", "auto");
			this.$drop_icon.addClass(class_name);
			this.$header_title.addClass(class_name);
			$(this.wrapper[0]).off("mouseleave");
			$(this.wrapper[0]).off("mouseover");
		} else {
			$(this.wrapper[0]).css("width", "100%");
			this.$drop_icon.removeClass(class_name);
			this.$header_title.removeClass(class_name);
			this.setup_hover();
		}
	}
};
