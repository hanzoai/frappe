import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import get_desktop_icons


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/app"
		raise frappe.Redirect

	context.icons = get_desktop_icons()
	return context
