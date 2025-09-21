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
frappe.pages["desktop"].on_page_show = function (wrapper) {};
function setup() {
	let desktop_icon_style = $("#icon-style").attr("data-icon-style");
	let navbar_style = $("#icon-style").attr("data-navbar-style");

	$(".desktop-icon").each((i, el) => {
		let icon_name = $(el).attr("data-icon");
		let icon_container = $(el.children[0]);

		if ($(el).attr("data-logo") != "None") {
			// create a img tag
			const logo_url = $(el).attr("data-logo");
			const $img = $("<img>").attr("src", logo_url);
			icon_container.append($img);
			icon_container.css("border", "none");
		} else {
			const svg = frappe.utils.icon(icon_name, "xl icon-stroke");

			if (svg) {
				const $svg = $(svg);

				// Apply stroke via CSS
				if (desktop_icon_style !== "Monochrome") {
					let bg_color, text_color;
					let color_scheme =
						frappe.palette[frappe.palette_map[icon_container.attr("data-color")]];
					if (desktop_icon_style === "Subtle") {
						bg_color = `var(${color_scheme[0]})`;
						text_color = color_scheme[1];
					} else if (desktop_icon_style === "Subtle Reverse") {
						bg_color = `var(${color_scheme[1]})`;
						text_color = color_scheme[0];
					} else if (desktop_icon_style === "Subtle Reverse w Opacity") {
						// #0289f7bd
						var style = window.getComputedStyle(document.body);
						console.log(style.getPropertyValue(color_scheme[1]));
						bg_color = style.getPropertyValue(color_scheme[1]) + "e6";
						text_color = color_scheme[0];
					}
					icon_container.css("background-color", `${bg_color}`);
					$svg.find("*").css("stroke", `var(${text_color})`);

					// Apply to svg root
					$svg.css("stroke", `var(${bg_color})`);
					icon_container.css("border", "none");
				}

				icon_container.append($svg);
			}
		}

		// let color_name = icon_container.attr("data-color");
		// icon_container.css("background-color", color_name);
	});
	setup_navbar(navbar_style);
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

function setup_navbar(navbar_style) {
	if (navbar_style != "Awesomebar") {
		$(".sticky-top > .navbar").hide();
	} else {
		$(".navbar").show();
	}
}

frappe.router.on("change", function () {
	if (frappe.get_route()[0] == "desktop") setup_navbar();
	else $(".navbar").show();
});

frappe.pages["desktop"].on_page_show = function () {
	let desktop_icon_style = $("#icon-style").attr("data-icon-style");
	let navbar_style = $("#icon-style").attr("data-navbar-style");
	setup_avatar();
	if (navbar_style != "Awesomebar") {
		if (navbar_style == "macOS Launchpad")
			$(".desktop-container").css("align-items", "normal");
		setup_avatar();
	}
};
function setup_avatar() {
	$(".desktop-avatar").html(frappe.avatar(frappe.session.user, "avatar-medium"));
}
