frappe.pages["desktop"].on_page_load = function (wrapper) {
	hide_sidebar();
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Desktop",
		single_column: true,
	});
	page.page_head.hide();
	$(frappe.render_template("desktop")).appendTo(page.body);
	setup();
};
function setup() {
	$(".desktop-icon").each((i, el) => {
		let icon_name = $(el).attr("data-icon");
		let icon_container = $(el.children[0]);
		const svg = frappe.utils.icon(icon_name, "xl");
		if (svg) {
			icon_container.html(svg);
		}
		// let color_name = icon_container.attr("data-color");
		// icon_container.css("background-color", color_name);
	});
	setup_click();
}

function setup_click() {
	$(".desktop-icon").on("click", (ev) => {
		let current = $(ev.currentTarget);
		if (current.attr("data-type") == "workspace") {
			window.location.href = window.location.origin + current.attr("data-route");
		} else {
			window.location.href = current.attr("data-route");
		}
	});
}

function hide_sidebar() {
	if (frappe.app.sidebar) {
		frappe.app.sidebar.wrapper.hide();
	}
}
