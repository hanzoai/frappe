import frappe
from frappe.modules import get_doctype_module
from frappe.utils.caching import site_cache

from .client import is_enabled, post_events

KEY = "pulse:active_apps"
EXPIRY = 60 * 60 * 12  # 12 hours


def log_app_heartbeat(req_params):
	if not is_enabled() or frappe.session.user in ("Guest", "Administrator"):
		return

	status_code = frappe.response.http_status_code or 0
	if status_code and not (200 <= status_code < 300):
		return

	method = req_params.get("method") or frappe.form_dict.get("method")
	doctype = req_params.get("doctype") or frappe.form_dict.get("doctype")

	if not method and not doctype:
		return

	app_name = None
	if method and "." in method and not method.startswith("frappe."):
		app_name = method.split(".", 1)[0]

	if not app_name and doctype:
		module = get_doctype_module(doctype)
		app_name = app_module_map().get(module)

	if app_name and app_name != "frappe":
		_mark_active(app_name)


def send():
	if not is_enabled():
		return

	active_apps = frappe.cache.get_value(KEY) or set()
	if not active_apps:
		return

	events = []
	for app in active_apps:
		events.append(
			{
				"name": "app_heartbeat",
				"app": app,
				"app_version": _get_app_version(app),
			}
		)

	try:
		if post_events(events):
			frappe.cache.delete_value(KEY)
	except Exception:
		frappe.log_error(title="Failed to send app heartbeat events")


def _mark_active(app):
	active_apps = frappe.cache.get_value(KEY) or set()
	if app not in active_apps:
		active_apps.add(app)
		frappe.cache.set_value(KEY, active_apps)
		ttl = frappe.cache.ttl(KEY)
		if ttl in (-1, None):
			frappe.cache.expire(KEY, EXPIRY)


def _get_app_version(app_name: str) -> str:
	try:
		return frappe.get_attr(app_name + ".__version__")
	except Exception:
		return "0.0.1"


@site_cache()
def app_module_map():
	defs = frappe.get_all("Module Def", fields=["name", "app_name"])
	return {d.name: d.app_name for d in defs}
