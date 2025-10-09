frappe.desktop_utils = {};
$.extend(frappe.desktop_utils, {
	modal: null,
	create_desktop_modal: function (icon, icon_title, icons_data, grid) {
		if (!this.modal) {
			this.modal = new DesktopModal(icon);
		}
		return this.modal;
	},
	close_desktop_modal: function () {
		if (this.modal) {
			this.modal.hide();
		}
	},
});
frappe.pages["desktop"].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Desktop",
		single_column: true,
		hide_sidebar: true,
	});
	let desktop_page = new DesktopPage(page);
	frappe.pages["desktop"].desktop_page = desktop_page;
	// setup();
};

function get_workspaces_from_app_name(app_name) {
	const app = frappe.boot.app_data.filter((a) => {
		return a.app_title === app_name;
	});
	if (app.length > 0) return app[0].workspaces;
}

function get_route(desktop_icon) {
	let route;
	if (!desktop_icon) return;
	let item = {};
	if (desktop_icon.type == "External" && desktop_icon.link) {
		route = window.location.origin + desktop_icon.link;
	} else {
		if (desktop_icon.type == "Workspace") {
			item = {
				type: desktop_icon.type,
				link: frappe.router.slug(desktop_icon.workspace),
			};
		} else if (desktop_icon.type == "List") {
			item = {
				type: desktop_icon.type,
				link: desktop_icon.__doctype,
			};
		}
		route = frappe.utils.generate_route(item);
	}

	return route;
}

frappe.pages["desktop"].on_page_show = function () {
	frappe.pages["desktop"].desktop_page.setup();
};

function toggle_icons(icons) {
	icons.forEach((i) => {
		$(i).parent().show();
	});
}

class DesktopPage {
	constructor(page) {
		this.prepare();
		this.make(page);
		this.setup();
	}

	prepare() {
		this.apps_icons = frappe.boot.desktop_icons.filter((c) => {
			return c.icon_type == "App" || c.icon_type == "Folder";
		});
	}

	make(page) {
		page.page_head.hide();
		$(frappe.render_template("desktop")).appendTo(page.body);
		this.wrapper = page.body.find(".desktop-container");
		this.icon_grid = new DesktopIconGrid(this.wrapper, this.apps_icons);
	}

	setup() {
		this.setup_avatar();
		this.setup_navbar();
		this.setup_icon_search();
		this.handke_route_change();
	}
	setup_avatar() {
		$(".desktop-avatar").html(frappe.avatar(frappe.session.user, "avatar-medium"));
	}
	setup_navbar() {
		$(".sticky-top > .navbar").hide();
	}

	handke_route_change() {
		const me = this;
		frappe.router.on("change", function () {
			if (frappe.get_route()[0] == "desktop") me.setup_navbar();
			else {
				$(".navbar").show();
				frappe.desktop_utils.close_desktop_modal();
			}
		});
	}

	setup_icon_search() {
		let all_icons = $(".icon-title");
		let icons_to_show = [];
		$(".desktop-search-wrapper > #navbar-search").on("input", function (e) {
			let search_query = $(e.target).val().toLowerCase();
			console.log(search_query);
			icons_to_show = [];
			all_icons.each(function (index, element) {
				$(element).parent().hide();
				let label = $(element).text().toLowerCase();
				if (label.includes(search_query)) {
					icons_to_show.push(element);
				}
			});
			toggle_icons(icons_to_show);
		});
	}
}

class DesktopIconGrid {
	constructor(wrapper, icons_data, row_size, in_folder, in_modal, parent_icon, no_dragging) {
		this.wrapper = wrapper;
		this.icons_data = icons_data;
		this.row_size = row_size;
		this.icons = [];
		this.page_size = {
			col: 4,
			row: 3,
			total: function () {
				return this.col * this.row;
			},
		};
		this.in_folder = in_folder;
		this.in_modal = in_modal;
		this.parent_icon_obj = parent_icon;
		this.no_dragging = no_dragging;
		this.grids = [];
		this.prepare();
		this.make();
	}
	prepare() {
		this.total_pages = Math.ceil(this.icons_data.length / this.page_size.total());
		this.icons_data_by_page = this.split_data(this.icons_data, this.page_size.total());
	}
	make() {
		const me = this;
		for (let i = 0; i < this.total_pages; i++) {
			let template = `<div class="icons"></div>`;

			if (this.row_size && this.in_modal) {
				template = `<div class="icons" style="display: none; grid-template-columns: repeat(${this.row_size}, 1fr)"></div>`;
			}
			this.grids.push($(template).appendTo(this.wrapper));
			this.make_icons(this.icons_data_by_page[i], this.grids[i]);
			if (!this.no_dragging) {
				this.setup_reordering(this.grids[i]);
			}
			this.grids[i].on("wheel", function (event) {
				if (event.originalEvent) {
					event = event.originalEvent; // for jQuery or wrapped events
				}

				if (Math.abs(event.deltaX) > Math.abs(event.deltaY)) {
					event.preventDefault();
					if (event.deltaX > 0) {
						if (me.current_page != me.total_pages - 1) me.current_page++;
						me.change_to_page(me.current_page);
					} else {
						if (me.current_page != 0) me.current_page--;
						me.change_to_page(me.current_page);
					}
				}
			});
		}
		this.setup_pagination();
	}
	setup_pagination() {
		this.current_page = 0;
		this.change_to_page(this.current_page);
	}
	change_to_page(index) {
		this.grids.forEach((g) => $(g).css("display", "none"));
		this.grids[index].css("display", "grid");
		this.current_page = index;
	}
	split_data(icons, size) {
		const result = [];

		for (let i = 0; i < icons.length; i += size) {
			result.push(icons.slice(i, i + size));
		}

		return result;
	}
	make_icons(icons_data, grid) {
		icons_data.forEach((icon) => {
			let icon_html = new DesktopIcon(icon, this.in_folder).get_desktop_icon_html();
			this.icons.push(icon_html);
			grid.append(icon_html);
		});
	}

	setup_reordering(grid) {
		const me = this;
		let sortable = new Sortable($(grid).get(0), {
			swapThreshold: 0.09,
			group: {
				name: "desktop",
				put: true,
				pull: true,
			},
			onEnd: function (evt) {
				let title = $(evt.item).find(".icon-title").text();
				if (me.parent_icon_obj) {
					let icon = me.parent_icon_obj.child_icons.findIndex((f) => f.label == title);
					me.parent_icon_obj.child_icons.splice(icon, 1);
					if (me.parent_icon_obj) me.parent_icon_obj.render_folder_thumbnail();
				}

				// if (evt.to.parentElement.classList.contains("folder-icon")) {
				// 	// open the folder

				// }
			},
		});
	}
}
class DesktopIcon {
	constructor(icon, in_folder) {
		this.icon_data = icon;
		this.icon_title = this.icon_data.label;
		this.icon_subtitle = "";
		this.icon_type = this.icon_data.icon_type;
		this.in_folder = in_folder;
		this.type = this.icon_data.type;
		if (this.icon_type != "Folder") {
			this.icon_route = get_route(this.get_desktop_icon(this.icon_title));
		}
		this.icon = $(
			frappe.render_template("desktop_icon", { icon: this.icon_data, in_folder: in_folder })
		);
		this.icon_caption_area = $(this.icon.get(0).children[1]);
		this.child_icons = this.get_child_icons_data();
		// this.child_icons = this.get_desktop_icon(this.icon_title).child_icons;
		// this.child_icons_data = this.get_child_icons_data();
		this.parent_icon = this.icon_data.icon;
		this.setup_click();
		this.setup_context_menu();
		this.render_folder_thumbnail();
		this.setup_dragging();
		this.child_icons = this.get_child_icons_data();
	}
	get_child_icons_data() {
		return frappe.boot.desktop_icons.filter((f) => {
			return f.parent_icon == this.icon_title;
		});
	}
	get_desktop_icon_html() {
		return this.icon;
	}
	get_desktop_icon(icon_label) {
		return frappe.boot.desktop_icons.find((d) => {
			return d.label == icon_label;
		});
	}
	setup_click() {
		const me = this;
		if (this.child_icons.length && (this.icon_type == "App" || this.icon_type == "Folder")) {
			$(this.icon).on("click", () => {
				let modal = frappe.desktop_utils.create_desktop_modal(me);
				modal.setup(me.icon_title, me.child_icons, 4);
				modal.show();
			});
			$($(this.icon_caption_area).children()[1]).html(
				`${this.child_icons.length} Workspaces`
			);
		} else {
			this.icon.attr("href", this.icon_route);
		}
	}

	setup_context_menu() {
		const me = this;
		this.context_menu_items = {
			icon: [
				{
					label: "Add Children Icon",
					icon: "add",
					onClick: function () {
						console.log("Open folder modal");
					},
				},
			],
		};
		this.context_menu = new ContextMenu(this.context_menu_items["icon"]);
		$(this.icon).on("contextmenu", function (event) {
			event.preventDefault();
			me.context_menu.show(event);
		});
	}

	render_folder_thumbnail() {
		if (this.icon_type == "Folder") {
			if (!this.folder_wrapper) this.folder_wrapper = this.icon.find(".icon-container");
			this.folder_wrapper.html("");
			this.folder_grid = new DesktopIconGrid(
				this.folder_wrapper,
				this.child_icons,
				4,
				true,
				true,
				null,
				true
			);
		}
	}

	setup_dragging() {
		this.icon.on("drag", (event) => {
			const mouse_x = event.clientX;
			const mouse_y = event.clientY;
			if (frappe.desktop_utils.modal) {
				let modal = frappe.desktop_utils.modal.modal
					.find(".modal-content")
					.get(0)
					.getBoundingClientRect();
				if (
					mouse_x > modal.right ||
					mouse_x < modal.left ||
					mouse_y > modal.bottom ||
					mouse_y < modal.top
				) {
					frappe.desktop_utils.close_desktop_modal();
				}
			}
		});
	}
}

class DesktopModal {
	constructor(icon) {
		this.parent_icon_obj = icon;
	}
	setup(icon_title, child_icons_data, grid_row_size) {
		const me = this;
		this.modal = new frappe.get_modal(icon_title, "");
		this.modal.find(".modal-header").addClass("desktop-modal-heading");
		this.modal.addClass("desktop-modal");
		this.modal.attr("draggable", true);
		this.modal.find(".modal-body").addClass("desktop-modal-body");
		this.$child_icons_wrapper = this.modal.find(".desktop-modal-body");

		this.child_icon_grid = new DesktopIconGrid(
			this.$child_icons_wrapper,
			child_icons_data,
			grid_row_size,
			false,
			true,
			this.parent_icon_obj
		);

		this.modal.on("hidden.bs.modal", function () {
			me.modal.remove();
		});
	}
	show() {
		this.modal.modal("show");
	}
	hide() {
		this.modal.modal("hide");
	}
}
class ContextMenu {
	constructor(menu_items) {
		this.template = $(`<div class="dropdown-menu desktop-context-menu" role="menu"></div>`);
		this.menu_items = menu_items;
		this.make();
	}
	make() {
		this.template.appendTo(document.body);
		this.menu_items.forEach((f) => {
			this.add_menu_item(f);
		});
	}
	add_menu_item(item) {
		$(`<div class="dropdown-menu-item">
			<a>
				<div class="sidebar-item-icon">
					${
						item.icon
							? frappe.utils.icon(item.icon)
							: `<img
							class="logo"
							src="${item.icon_url}"
						>`
					}
				</div>
				<span class="menu-item-title">${item.label}</span>
			</a>
		</div>`)
			.on("click", function () {
				item.onClick();
				this.template;
			})
			.appendTo(this.template);
	}
	show(event) {
		this.top = this.mouseY(event) + "px";
		this.left = this.mouseX(event) + "px";
		this.template.css("display", "block");
		this.template.css("top", this.top);
		this.template.css("left", this.left);
	}
	mouseX(evt) {
		if (evt.pageX) {
			return evt.pageX;
		} else if (evt.clientX) {
			return (
				evt.clientX +
				(document.documentElement.scrollLeft
					? document.documentElement.scrollLeft
					: document.body.scrollLeft)
			);
		} else {
			return null;
		}
	}

	mouseY(evt) {
		if (evt.pageY) {
			return evt.pageY;
		} else if (evt.clientY) {
			return (
				evt.clientY +
				(document.documentElement.scrollTop
					? document.documentElement.scrollTop
					: document.body.scrollTop)
			);
		} else {
			return null;
		}
	}
}
