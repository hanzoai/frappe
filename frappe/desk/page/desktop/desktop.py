import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import get_desktop_icons


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/app"
		raise frappe.Redirect
	context.desktop_icon_style = frappe.get_single_value("Desktop Settings", "icon_style")
	context.navbar_style = frappe.get_single_value("Desktop Settings", "navbar_style")
	context.brand_logo = frappe.get_single_value("Navbar Settings", "app_logo")
	context.current_user = frappe.session.user
	context.icons = get_desktop_icons()
	return context
