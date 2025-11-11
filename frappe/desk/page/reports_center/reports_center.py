from json import dumps

import frappe
from frappe.boot import get_allowed_pages, get_allowed_reports


@frappe.whitelist()
def get_reports(module_name=None):
	reports_info = []
	if module_name:
		report_center = frappe.get_doc("Report Center", module_name)
		for report_links in report_center.links:
			if report_links.report in get_allowed_reports().keys():
				reports_info.append(get_allowed_reports()[report_links.report])
		return reports_info
