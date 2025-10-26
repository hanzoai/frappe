import "../dom";
frappe.provide("frappe.ui");

frappe.ui.menu = class ContextMenu {
	constructor(menu_items) {
		this.template = $(`<div class="dropdown-menu context-menu" role="menu"></div>`);
		this.menu_items = menu_items;
	}

	make() {
		this.template.empty(); // clear old

		this.menu_items.forEach((f) => {
			this.add_menu_item(f);
		});

		if ($(".context-menu").length === 0) {
			this.template.appendTo(document.body);
		} else {
			this.template = $(".context-menu");
		}
	}
	add_menu_item(item) {
		const me = this;
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
				setTimeout(function () {
					if (me.visible) {
						me.hide();
					}
				}, 1000);
			})
			.appendTo(this.template);
	}
	show(element) {
		this.close_all_other_menu();

		this.make();

		const offset = $(element).offset();
		const height = $(element).outerHeight();

		this.template.css({
			display: "block",
			position: "absolute",
			top: offset.top + height + "px", // just below the element
			left: offset.left + "px", // align to the left of the element
		});

		this.visible = true;
	}
	close_all_other_menu() {
		$(".context-menu").hide();
	}
	hide() {
		this.template.css("display", "none");
		this.visible = false;
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
};

frappe.ui.create_menu = function attachContextMenuToElement(
	elementSelector,
	menuItems,
	right_click
) {
	const contextMenu = new frappe.ui.menu(menuItems);
	if (right_click) {
		// Show menu on right-click or click (choose what suits you)
		$(elementSelector).on("contextmenu", function (event) {
			event.preventDefault();
			event.stopPropagation(); // Prevents bubbling up
			if (contextMenu.visible) {
				contextMenu.hide();
			} else {
				contextMenu.show(this);
			}
		});
	} else {
		// Show menu on right-click or click (choose what suits you)
		$(elementSelector).on("click", function (event) {
			event.preventDefault();
			event.stopPropagation(); // Prevents bubbling up
			if (contextMenu.visible) {
				contextMenu.hide();
			} else {
				contextMenu.show(this);
			}
		});
	}

	// Hide menu on outside click
	$(document).on("click", function () {
		if (contextMenu.visible) {
			contextMenu.hide();
		}
	});

	// Optional: hide on ESC key
	$(document).on("keydown", function (e) {
		if (e.key === "Escape" && contextMenu.visible) {
			contextMenu.hide();
		}
	});
};
