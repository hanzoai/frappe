# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import frappe
from frappe import _
from frappe.utils.response import is_traceback_allowed

no_cache = 1


def get_context(context):
	if frappe.flags.in_migrate:
		return

<<<<<<< HEAD
	allow_traceback = frappe.get_system_settings("allow_error_traceback") if frappe.db else False

	context.error_title = context.error_title or _("Uncaught Server Exception")
	context.error_message = context.error_message or _("There was an error building this page")
=======
	if not context.title:
		context.title = _("Server Error")
	if not context.message:
		context.message = _("There was an error building this page")
>>>>>>> f4062b4d7a (fix: ensure consistent error in response)

	return {
		"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;")
		if is_traceback_allowed()
		else ""
	}
