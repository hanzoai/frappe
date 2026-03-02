# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import frappe
from frappe import _
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.utils import cint
from frappe.utils.jinja_globals import is_rtl
from frappe.www.printview import (
	get_print_format_doc,
	get_print_style,
	get_rendered_template,
	set_link_titles,
	trigger_print_script,
)

no_cache = 1

MAX_CONSOLIDATED_PRINT_DOCS = 100


def get_context(context):
	"""Build context for consolidated (multi-document, no page-break) print."""
	doctype = frappe.form_dict.get("doctype")
	names_json = frappe.form_dict.get("names")

	if not doctype or not names_json:
		return {
			"body": "<h1>Error</h1><p>Parameters <code>doctype</code> and <code>names</code> are required.</p>",
			"print_style": "",
			"title": "Error",
			"lang": "en",
			"layout_direction": "ltr",
			"doc_count": 0,
		}

	try:
		names = json.loads(names_json)
	except (json.JSONDecodeError, TypeError):
		frappe.throw(_("Invalid names parameter: must be a JSON array of document names"))

	if not isinstance(names, list) or len(names) == 0:
		frappe.throw(_("At least one document name is required"))

	if len(names) > MAX_CONSOLIDATED_PRINT_DOCS:
		frappe.throw(
			_("Cannot consolidate more than {0} documents at a time").format(MAX_CONSOLIDATED_PRINT_DOCS)
		)

	format_name = frappe.form_dict.get("format") or None
	no_letterhead = frappe.form_dict.get("no_letterhead", 0)
	letterhead = frappe.form_dict.get("letterhead") or None
	trigger_print = cint(frappe.form_dict.get("trigger_print", 0))

	meta = frappe.get_meta(doctype)
	print_format = get_print_format_doc(format_name, meta=meta)

	all_html_parts = []

	for name in names:
		try:
			doc = frappe.get_lazy_doc(doctype, name)
			set_link_titles(doc)
			html = _get_doc_print_html(doc, print_format, meta, no_letterhead, letterhead)
			all_html_parts.append(html)
		except frappe.PermissionError:
			frappe.log_error(
				title="Consolidated Print Permission Error",
				message=f"No permission to print {doctype} {name}",
			)
		except Exception:
			frappe.log_error(
				title="Consolidated Print Render Error",
				message=f"Error rendering {doctype} {name}",
			)

	separator = '<div class="consolidated-doc-separator print-hide"></div>'
	body = separator.join(
		f'<div class="consolidated-doc">{html}</div>' for html in all_html_parts
	)

	if trigger_print:
		body += trigger_print_script

	make_access_log(
		doctype=doctype,
		document=", ".join(names[:10]),
		file_type="PDF",
		method="Print",
		page=f"Consolidated Print Format: {getattr(print_format, 'name', 'Standard')} ({len(names)} docs)",
	)

	return {
		"body": body,
		"print_style": get_print_style(frappe.form_dict.get("style"), print_format),
		"title": f"Consolidated Print — {doctype}",
		"lang": frappe.local.lang,
		"layout_direction": "rtl" if is_rtl() else "ltr",
		"doctype": doctype,
		"doc_count": len(all_html_parts),
	}


def _get_doc_print_html(doc, print_format, meta, no_letterhead, letterhead):
	"""Return rendered HTML for a single document, handling both standard and beta print formats."""
	if print_format and print_format.get("print_format_builder_beta"):
		from frappe.utils.weasyprint import get_html

		return get_html(doctype=doc.doctype, name=doc.name, print_format=print_format.name)

	return get_rendered_template(
		doc=doc,
		print_format=print_format,
		meta=meta,
		no_letterhead=no_letterhead,
		letterhead=letterhead,
		trigger_print=False,
	)
