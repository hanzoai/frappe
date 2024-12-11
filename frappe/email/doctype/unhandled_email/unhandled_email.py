# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class UnhandledEmail(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		email_account: DF.Link | None
		message_id: DF.Code | None
		raw: DF.Code | None
		reason: DF.LongText | None
		uid: DF.Data | None
	# end: auto-generated types

	@staticmethod
	def clear_old_logs(days=30):
		frappe.db.delete(
			"Unhandled Email",
			{
				"modified": ("<", frappe.utils.add_days(frappe.utils.nowdate(), -1 * days)),
			},
		)
=======
	pass


def remove_old_unhandled_emails():
	frappe.db.delete(
		"Unhandled Email", {"modified": ("<", frappe.utils.add_days(frappe.utils.nowdate(), -14))}
	)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
