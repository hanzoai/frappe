# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.model.document import Document


class OAuthProviderSettings(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		skip_authorization: DF.Literal["Force", "Auto"]
	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	pass


def get_oauth_settings():
	"""Returns oauth settings"""
<<<<<<< HEAD
	return frappe._dict(
		{"skip_authorization": frappe.db.get_single_value("OAuth Provider Settings", "skip_authorization")}
	)
=======
	out = frappe._dict(
		{"skip_authorization": frappe.db.get_single_value("OAuth Provider Settings", "skip_authorization")}
	)

	return out
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
