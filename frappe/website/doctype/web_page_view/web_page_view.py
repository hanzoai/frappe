# Copyright (c) 2020, Frappe Technologies and contributors
# License: MIT. See LICENSE

<<<<<<< HEAD
from urllib.parse import urlparse

import frappe
import frappe.utils
=======
import frappe
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
from frappe.model.document import Document


class WebPageView(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		browser: DF.Data | None
		browser_version: DF.Data | None
		campaign: DF.Data | None
		is_unique: DF.Data | None
		medium: DF.Data | None
		path: DF.Data | None
		referrer: DF.Data | None
		source: DF.Data | None
		time_zone: DF.Data | None
		user_agent: DF.Data | None
		visitor_id: DF.Data | None

	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=180):
		from frappe.query_builder import Interval
		from frappe.query_builder.functions import Now

		table = frappe.qb.DocType("Web Page View")
		frappe.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))


@frappe.whitelist(allow_guest=True)
def make_view_log(
	referrer=None,
	browser=None,
	version=None,
	user_tz=None,
	source=None,
	campaign=None,
	medium=None,
	visitor_id=None,
):
	if not is_tracking_enabled():
		return

	# real path
	path = frappe.request.headers.get("Referer")

	if not frappe.utils.is_site_link(path):
		return

	path = urlparse(path).path

=======
	pass


@frappe.whitelist(allow_guest=True)
def make_view_log(path, referrer=None, browser=None, version=None, url=None, user_tz=None):
	if not is_tracking_enabled():
		return

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	request_dict = frappe.request.__dict__
	user_agent = request_dict.get("environ", {}).get("HTTP_USER_AGENT")

	if referrer:
		referrer = referrer.split("?", 1)[0]

<<<<<<< HEAD
	if path != "/" and path.startswith("/"):
		path = path[1:]

	if path.startswith(("api/", "app/", "assets/", "private/files/")):
		return

	is_unique = visitor_id and not bool(frappe.db.exists("Web Page View", {"visitor_id": visitor_id}))

=======
	is_unique = True
	if referrer.startswith(url):
		is_unique = False

	if path != "/" and path.startswith("/"):
		path = path[1:]

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	view = frappe.new_doc("Web Page View")
	view.path = path
	view.referrer = referrer
	view.browser = browser
	view.browser_version = version
	view.time_zone = user_tz
	view.user_agent = user_agent
	view.is_unique = is_unique
<<<<<<< HEAD
	view.source = source
	view.campaign = campaign
	view.medium = (medium or "").lower()
	view.visitor_id = visitor_id
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	try:
		if frappe.flags.read_only:
			view.deferred_insert()
		else:
			view.insert(ignore_permissions=True)
	except Exception:
<<<<<<< HEAD
		frappe.clear_last_message()
=======
		if frappe.message_log:
			frappe.message_log.pop()
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


@frappe.whitelist()
def get_page_view_count(path):
	return frappe.db.count("Web Page View", filters={"path": path})


def is_tracking_enabled():
	return frappe.db.get_single_value("Website Settings", "enable_view_tracking")
