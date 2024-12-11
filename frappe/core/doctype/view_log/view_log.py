# Copyright (c) 2018, Frappe Technologies and contributors
# License: MIT. See LICENSE

<<<<<<< HEAD
import frappe
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
from frappe.model.document import Document


class ViewLog(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		viewed_by: DF.Data | None

	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=180):
		from frappe.query_builder import Interval
		from frappe.query_builder.functions import Now

		table = frappe.qb.DocType("View Log")
		frappe.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))
=======
	pass
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
