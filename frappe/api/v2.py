"""REST API v2

This file defines routes and implementation for REST API.

Note:
	- All functions in this file should be treated as "whitelisted" as they are exposed via routes
	- None of the functions present here should be called from python code, their location and
	  internal implementation can change without treating it as "breaking change".
"""
import json
from typing import Any

from werkzeug.routing import Rule

import frappe
import frappe.client
from frappe import _, get_newargs, is_whitelisted
from frappe.core.doctype.server_script.server_script_utils import get_server_script_map
from frappe.desk.form.load import get_attachments, get_tags
from frappe.desk.form.utils import remove_attach
from frappe.handler import is_valid_http_method, run_server_script, upload_file
from frappe.share import get_users as get_shared_users

PERMISSION_MAP = {
	"GET": "read",
	"POST": "write",
}


def handle_rpc_call(method: str, doctype: str | None = None):
	from frappe.modules.utils import load_doctype_module

	if doctype:
		# Expand to run actual method from doctype controller
		module = load_doctype_module(doctype)
		method = module.__name__ + "." + method

	for hook in reversed(frappe.get_hooks("override_whitelisted_methods", {}).get(method, [])):
		# override using the last hook
		method = hook
		break

	# via server script
	server_script = get_server_script_map().get("_api", {}).get(method)
	if server_script:
		return run_server_script(server_script)

	try:
		method = frappe.get_attr(method)
	except Exception as e:
		frappe.throw(_("Failed to get method {0} with {1}").format(method, e))

	is_whitelisted(method)
	is_valid_http_method(method)

	return frappe.call(method, **frappe.form_dict)


def login():
	"""Login happens implicitly, this function doesn't do anything."""
	pass


def logout():
	frappe.local.login_manager.logout()
	frappe.db.commit()


def read_doc(doctype: str, name: str):
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	doc.apply_fieldlevel_read_permissions()
	return doc


def document_list(doctype: str):
	if frappe.form_dict.get("fields"):
		frappe.form_dict["fields"] = json.loads(frappe.form_dict["fields"])

	# set limit of records for frappe.get_list
	frappe.form_dict.limit_page_length = frappe.form_dict.limit or 20
	# evaluate frappe.get_list
	return frappe.call(frappe.client.get_list, doctype, **frappe.form_dict)


def count(doctype: str) -> int:
	from frappe.desk.reportview import get_count

	frappe.form_dict.doctype = doctype

	return get_count()


def create_doc(doctype: str):
	data = frappe.form_dict
	data.pop("doctype", None)
	return frappe.new_doc(doctype, **data).insert()


def update_doc(doctype: str, name: str):
	data = frappe.form_dict

	doc = frappe.get_doc(doctype, name, for_update=True)
	data.pop("flags", None)
	doc.update(data)
	doc.save()

	# check for child table doctype
	if doc.get("parenttype"):
		frappe.get_doc(doc.parenttype, doc.parent).save()

	return doc


def delete_doc(doctype: str, name: str):
	frappe.client.delete_doc(doctype, name)
	frappe.response.http_status_code = 202
	return "ok"


def add_attachment(doctype: str, name: str):
	frappe.form_dict.update({"doctype": doctype, "docname": name})
	return upload_file()


def add_tag(doctype: str, name: str):
	from frappe.desk.doctype.tag.tag import add_tag

	return add_tag(frappe.form_dict.tag, doctype, name)


def remove_tag(doctype: str, name: str):
	from frappe.desk.doctype.tag.tag import remove_tag

	return remove_tag(frappe.form_dict.tag, doctype, name)


def get_assignments(doctype: str, name: str):
	from frappe.desk.form.assign_to import get

	return get({"doctype": doctype, "name": name})


def add_assignment(doctype: str, name: str):
	from frappe.desk.form.assign_to import add

	return add(
		{
			"doctype": doctype,
			"name": name,
			"assign_to": frappe.form_dict.assign_to,
		}
	)


def remove_assignment(doctype: str, name: str):
	from frappe.desk.form.assign_to import remove

	return remove(doctype, name, frappe.form_dict.assigned_to)


def add_share(doctype: str, name: str):
	from frappe.share import add as add_share

	return add_share(
		doctype,
		name,
		user=frappe.form_dict.user,
		read=frappe.form_dict.read,
		write=frappe.form_dict.write,
		submit=frappe.form_dict.submit,
		share=frappe.form_dict.share,
		everyone=frappe.form_dict.everyone,
		notify=frappe.form_dict.notify,
	)


def update_share(doctype: str, name: str):
	from frappe.share import set_permission

	return set_permission(
		doctype,
		name,
		frappe.form_dict.user,
		frappe.form_dict.permission_to,
		frappe.form_dict.value,
		frappe.form_dict.everyone,
	)


def get_meta(doctype: str):
	frappe.only_for("All")
	return frappe.get_meta(doctype)


def execute_doc_method(doctype: str, name: str, method: str | None = None):
	"""Get a document from DB and execute method on it.

	Use cases:
	- Submitting/cancelling document
	- Triggering some kind of update on a document
	"""
	method = method or frappe.form_dict.pop("run_method")
	doc = frappe.get_doc(doctype, name)
	doc.is_whitelisted(method)

	doc.check_permission(PERMISSION_MAP[frappe.request.method])
	return doc.run_method(method, **frappe.form_dict)


def run_doc_method(method: str, document: dict[str, Any] | str, kwargs=None):
	"""run a whitelisted controller method on in-memory document.


	This is useful for building clients that don't necessarily encode all the business logic but
	call server side function on object to validate and modify the doc.

	The doc CAN exists in DB too and can write to DB as well if method is POST.
	"""

	if isinstance(document, str):
		document = frappe.parse_json(document)

	if kwargs is None:
		kwargs = {}

	doc = frappe.get_doc(document)
	doc._original_modified = doc.modified
	doc.check_if_latest()

	doc.check_permission(PERMISSION_MAP[frappe.request.method])

	method_obj = getattr(doc, method)
	fn = getattr(method_obj, "__func__", method_obj)
	is_whitelisted(fn)
	is_valid_http_method(fn)

	new_kwargs = get_newargs(fn, kwargs)
	response = doc.run_method(method, **new_kwargs)
	frappe.response.docs.append(doc)  # send modified document and result both.
	return response


url_rules = [
	# RPC calls
	Rule("/method/login", endpoint=login),
	Rule("/method/logout", endpoint=logout),
	Rule("/method/ping", endpoint=frappe.ping),
	Rule("/method/upload_file", endpoint=upload_file),
	Rule("/method/<method>", endpoint=handle_rpc_call),
	Rule(
		"/method/run_doc_method",
		methods=["GET", "POST"],
		endpoint=lambda: frappe.call(run_doc_method, **frappe.form_dict),
	),
	Rule("/method/<doctype>/<method>", endpoint=handle_rpc_call),
	# Document level APIs
	Rule("/document/<doctype>", methods=["GET"], endpoint=document_list),
	Rule("/document/<doctype>", methods=["POST"], endpoint=create_doc),
	Rule("/document/<doctype>/<path:name>/", methods=["GET"], endpoint=read_doc),
	Rule("/document/<doctype>/<path:name>/", methods=["PATCH", "PUT"], endpoint=update_doc),
	Rule("/document/<doctype>/<path:name>/", methods=["DELETE"], endpoint=delete_doc),
	Rule("/document/<doctype>/<path:name>/attachments", methods=["GET"], endpoint=get_attachments),
	Rule("/document/<doctype>/<path:name>/attachment", methods=["POST"], endpoint=add_attachment),
	Rule("/document/<doctype>/<path:name>/attachment", methods=["DELETE"], endpoint=remove_attach),
	Rule("/document/<doctype>/<path:name>/tags", methods=["GET"], endpoint=get_tags),
	Rule("/document/<doctype>/<path:name>/tag", methods=["POST"], endpoint=add_tag),
	Rule("/document/<doctype>/<path:name>/tag", methods=["DELETE"], endpoint=remove_tag),
	Rule("/document/<doctype>/<path:name>/assignments", methods=["GET"], endpoint=get_assignments),
	Rule("/document/<doctype>/<path:name>/assignment", methods=["POST"], endpoint=add_assignment),
	Rule("/document/<doctype>/<path:name>/assignment", methods=["DELETE"], endpoint=remove_assignment),
	Rule("/document/<doctype>/<path:name>/shares", methods=["GET"], endpoint=get_shared_users),
	Rule("/document/<doctype>/<path:name>/share", methods=["POST"], endpoint=add_share),
	Rule("/document/<doctype>/<path:name>/share", methods=["PUT"], endpoint=update_share),
	Rule(
		"/document/<doctype>/<path:name>/method/<method>/",
		methods=["GET", "POST"],
		endpoint=execute_doc_method,
	),
	# Collection level APIs
	Rule("/doctype/<doctype>/meta", methods=["GET"], endpoint=get_meta),
	Rule("/doctype/<doctype>/count", methods=["GET"], endpoint=count),
]
