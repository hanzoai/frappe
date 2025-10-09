import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import get_desktop_icons


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/app"
		raise frappe.Redirect
	context.brand_logo = frappe.get_single_value("Navbar Settings", "app_logo")
	context.current_user = frappe.session.user
	return context
