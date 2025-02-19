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

	return {"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;")}
=======
	if not context.title:
		context.title = _("Server Error")
	if not context.message:
		context.message = _("There was an error building this page")

	allow_traceback = is_traceback_allowed() and not frappe.local.dev_server

	return {
		"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;") if allow_traceback else ""
	}
>>>>>>> f4062b4d7a (fix: ensure consistent error in response)
