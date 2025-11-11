# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ReportCenter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.desk.doctype.report_center_link.report_center_link import ReportCenterLink
		from frappe.types import DF

		links: DF.Table[ReportCenterLink]
		sidebar: DF.Link | None
	# end: auto-generated types
	pass
