import frappe
from frappe.model.sync import check_if_record_exists


def execute():
	for sidebar in frappe.get_all("Workspace Sidebar", pluck="name"):
		sidebar_doc = frappe.get_doc("Workspace Sidebar", sidebar)
		if sidebar_doc.app and check_if_record_exists(
			"app", frappe.get_app_path(sidebar_doc.app), "Workspace Sidebar", sidebar_doc.name
		):
			sidebar_doc.standard = 1
			sidebar_doc.save()
