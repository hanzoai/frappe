import time
from contextlib import suppress

from orjson import JSONDecodeError

import frappe
from frappe.utils import get_request_session
from frappe.utils.caching import site_cache
from frappe.utils.frappecloud import on_frappecloud

from .utils import anonymize_user, ensure_http, parse_interval, utc_iso


@frappe.whitelist()
@site_cache()
def is_enabled() -> bool:
	return bool(
		not frappe.conf.get("developer_mode", 0)
		and frappe.conf.get("pulse_api_key")
		and on_frappecloud()
		and frappe.get_system_settings("enable_telemetry")
	)


@frappe.whitelist(allow_guest=True)
def capture(event_name, site=None, app=None, user=None, properties=None, interval=None):
	if not is_enabled():
		return

	try:
		event_key = f"{event_name}:{site or None}:{app or None}:{user or None}"
		if _is_ratelimited(event_key, interval):
			return

		_queue_event(
			{
				"event_name": event_name,
				"captured_at": utc_iso(),
				"app": app,
				"user": anonymize_user(user),
				"site": site or frappe.local.site,
				"properties": properties,
			}
		)
		_update_ratelimit(event_key, interval)
	except Exception as e:
		frappe.logger("pulse").error(f"pulse-client - capture failed: {e!s}")


@frappe.whitelist(allow_guest=True)
def bulk_capture(events):
	if not is_enabled():
		return

	for event in events:
		try:
			# not supporting rate-limiting for bulk events
			# so queue all events as-is
			_queue_event(
				{
					"event_name": event.get("event_name"),
					"captured_at": event.get("captured_at") or utc_iso(),
					"site": frappe.local.site,
					"app": event.get("app"),
					"user": anonymize_user(event.get("user")),
					"properties": event.get("properties"),
				}
			)
		except Exception as e:
			frappe.logger("pulse").error(f"pulse-client - bulk capture failed for event {event}: {e!s}")


def _is_ratelimited(event_key, interval):
	if not interval:
		return False

	interval_seconds = parse_interval(interval)
	last_sent_key = f"pulse-client:last_sent:{event_key}"
	last_sent = frappe.cache.get_value(last_sent_key)

	if last_sent and time.monotonic() - float(last_sent) < interval_seconds:
		return True

	return False


def _update_ratelimit(event_key, interval):
	if not interval:
		return
	last_sent_key = f"pulse-client:last_sent:{event_key}"
	frappe.cache.set_value(last_sent_key, time.monotonic())


def _queue_event(event):
	frappe.cache.lpush("pulse-client:events", frappe.as_json(event))
	frappe.cache.ltrim("pulse-client:events", 0, 9999)


def queue_length():
	return frappe.cache.llen("pulse-client:events")


def send_queued_events():
	batch_size = 100
	max_batches = 10
	for _ in range(max_batches):
		events = collect_events(batch_size)
		if not events:
			break
		try:
			if not post(events):
				frappe.logger().error("Pulse sending events failed: non-2xx response")
		except Exception as e:
			frappe.logger().error(f"Pulse sending events failed: {e!s}")


def collect_events(batch_size=100):
	"""Pop batch of events from the queue"""
	events = []
	for _ in range(batch_size):
		event_json = frappe.cache.rpop("pulse-client:events")
		if not event_json:
			break
		data = decode_event(event_json)
		if data:
			events.append(data)
	return events


def decode_event(event_json):
	event_json = event_json.decode()
	with suppress(JSONDecodeError):
		return frappe.parse_json(event_json)


def post(events):
	# TODO: implement retry logic
	session = _create_session()
	url = _get_ingest_url()
	data = frappe.as_json({"events": events})
	resp = session.post(url, data=data, timeout=15)
	return 200 <= resp.status_code < 300


def _create_session():
	api_key = frappe.conf.get("pulse_api_key")
	session = get_request_session()
	session.headers.update(
		{
			"Content-Type": "application/json",
			"X-Pulse-API-Key": api_key,
		}
	)
	return session


def _get_ingest_url():
	host = frappe.conf.get("pulse_host") or "https://pulse.m.frappe.cloud"
	host = ensure_http(host)
	host = host.rstrip("/")

	endpoint = frappe.conf.get("pulse_ingest_endpoint") or "/api/method/pulse.api.bulk_ingest"
	endpoint = endpoint.lstrip("/")

	return f"{host}/{endpoint}"


@frappe.whitelist()
def get_debug_info(fetch_events=None, fetch_rate_limited_events=None):
	frappe.only_for("System Manager")

	info = frappe._dict()
	info.is_enabled = is_enabled()

	if info.is_enabled:
		info.queued_event_count = queue_length()

		if fetch_events:
			info.queued_events = []
			limit = int(fetch_events) if str(fetch_events).isdigit() else 20
			for _ in range(min(limit, info.queued_event_count)):
				event_json = frappe.cache.lindex("pulse-client:events", _)
				data = decode_event(event_json)
				if data:
					info.queued_events.append(data)

		if fetch_rate_limited_events:
			info.rate_limited_events = []
			limit = int(fetch_rate_limited_events) if str(fetch_rate_limited_events).isdigit() else 20
			for key in frappe.cache.get_keys("pulse-client:last_sent:*")[:limit]:
				last_sent = frappe.cache.get_value(key)
				event_key = key.replace("pulse-client:last_sent:", "")
				info.rate_limited_events.append(
					{
						"event_key": event_key,
						"last_sent": last_sent,
					}
				)

	return info
