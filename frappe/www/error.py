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
	context.error_title = context.error_title or _("Uncaught Server Exception")
	context.error_message = context.error_message or _("There was an error building this page")
=======
	allow_traceback = frappe.get_system_settings("allow_error_traceback") if frappe.db else False
	if frappe.local.flags.disable_traceback and not frappe.local.dev_server:
		allow_traceback = False

	if not context.title:
		context.title = _("Server Error")
	if not context.message:
		context.message = _("There was an error building this page")
>>>>>>> cef8c12ee4 (fix(style): fix oauth authorisation page and standardise error responses)

	return {
		"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;")
		if is_traceback_allowed()
		else ""
	}
