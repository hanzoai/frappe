frappe.pages["reports-center"].on_page_load = async function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Reports Center",
		single_column: true,
	});

	page.page_head.hide();
	let module = frappe.route_options?.module;
	let reports_data;
	$(frappe.render_template("reports_center")).appendTo(page.body);
	await frappe.call({
		method: "frappe.desk.page.reports_center.reports_center.get_reports",
		args: {
			module_name: module,
		},
		callback: function (r) {
			reports_data = r.message;
			render_list(module, reports_data);
		},
	});

	// $('.report-name').on('click', function() {
	//     const report_name = $(this).data('report');
	//     frappe.set_route('query-report', report_name);
	// });
};

function render_list(module_name, reports) {
	let module_name_wrapper = $(".module-name");
	module_name_wrapper.text(module_name);
	const container = $(".report-links");
	container.empty();
	if (!reports || Object.keys(reports).length === 0) {
		container.append(`<div class="text-muted">No reports found.</div>`);
		return;
	}

	Object.values(reports).forEach((report_data) => {
		const report_html = `
                <div class='report-details'>
                <div class="report-name fw-bold" data-report="${report_data.title}">${report_data.title}</div>
                </div>
        `;
		container.append(report_html);
	});

	// Optional: Add click handler
	container.find(".report-name").on("click", function () {
		const report_name = $(this).data("report");
		frappe.set_route("query-report", report_name);
	});
}

frappe.pages["reports-center"].on_page_show = function (wrapper) {
	// if (frappe.has_route_options()) {
	//     let module = frappe.route_options?.module;
	//     if (module) {
	//         const filtered = Object.fromEntries(
	//             Object.entries(frappe.boot.allowed_reports).filter(
	//                 ([, value]) => value.module === module
	//             )
	//         );
	//         console.log("Filtered Reports:", filtered);
	//         render_list(module,filtered);
	//     } else {
	//         render_list(module, frappe.boot.allowed_reports);
	//     }
	// } else {
	//     render_list(frappe.boot.allowed_reports);
	// }
};
