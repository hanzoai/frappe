import frappe
from frappe.website.utils import build_response


class RedirectPage:
	def __init__(self, path, http_status_code=301):
		self.path = path
		self.http_status_code = http_status_code

	def can_render(self):
		return True

	def render(self):
		return build_response(
			self.path,
			"",
<<<<<<< HEAD
			self.http_status_code,
=======
			301,
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			{
				"Location": frappe.flags.redirect_location or (frappe.local.response or {}).get("location"),
				"Cache-Control": "no-store, no-cache, must-revalidate",
			},
		)
