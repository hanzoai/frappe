from datetime import datetime, timezone

import frappe
from frappe.utils import get_request_session
from frappe.utils.caching import site_cache
from frappe.utils.frappecloud import on_frappecloud


@site_cache()
def is_enabled() -> bool:
	return (
		not frappe.conf.get("developer_mode", 0)
		and not frappe.conf.get("pulse_disabled", 0)
		and frappe.conf.get("pulse_api_key")
		and on_frappecloud()
		and frappe.get_system_settings("enable_telemetry")
	)


def post_events(events):
	events = _sanitize_events(events)
	session = _create_session()
	resp = session.post(_get_ingest_url(), data=events, timeout=5.0)
	return 200 <= resp.status_code < 300


def _create_session():
	api_key = frappe.conf.get("pulse_api_key")
	session = get_request_session()
	if api_key:
		session.headers.update({"Authorization": f"Bearer {api_key}"})
	return session


def _get_ingest_url():
	host = frappe.conf.get("pulse_host") or "https://pulse.m.frappe.cloud"
	if not host.startswith("http"):
		host = "https://" + host
	host = host.rstrip("/")

	endpoint = frappe.conf.get("pulse_ingest_endpoint") or "/api/method/pulse.api.ingest"
	endpoint = endpoint.lstrip("/")

	return f"{host}/{endpoint}"


def _sanitize_events(events):
	_events = []
	if not isinstance(events, list):
		_events = [events]

	for event in events:
		if not isinstance(event, dict) or "name" not in event:
			continue
		event["site"] = event["site"] or frappe.local.site
		event["timestamp"] = event["timestamp"] or _utc_iso()
		event["frappe_version"] = event["frappe_version"] or _get_frappe_version()
		_events.append(event)

	return _events


def _get_frappe_version() -> str:
	return getattr(frappe, "__version__", "unknown")


def _utc_iso() -> str:
	return datetime.now(timezone.utc).isoformat(timespec="seconds")
