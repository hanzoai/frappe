frappe.pages["desktop"].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Desktop",
		single_column: true,
		hide_sidebar: true,
	});
	page.page_head.hide();
	$(frappe.render_template("desktop")).appendTo(page.body);
	setup();
};
function setup() {
	$(".desktop-icon").each((i, el) => {
		let icon_name = $(el).attr("data-icon");
		let icon_container = $(el.children[0]);
		const link = $("<a>", {
			href: get_route($(el)),
		});

		const svg = frappe.utils.icon(icon_name, "xl");
		if (svg) {
			link.html(svg);
		}

		icon_container.append(link);
		// let color_name = icon_container.attr("data-color");
		// icon_container.css("background-color", color_name);
	});
}

function get_route(element) {
	let route;
	if (element.attr("data-type") == "workspace") {
		route = window.location.origin + element.attr("data-route");
	} else {
		route = element.attr("data-route");
	}
	return route;
}
