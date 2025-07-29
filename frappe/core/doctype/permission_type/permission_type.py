# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PermissionType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicable_for: DF.Link | None
	# end: auto-generated types

	def on_update(self):
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field

		if not frappe.db.exists(
			"Custom DocPerm",
			{
				"fieldname": self.name,
				"reference_doctype": self.applicable_for,
			},
		):
			# create custom field in Custom DocPerm
			create_custom_field(
				"Custom DocPerm",
				{
					"fieldname": self.name,
					"label": self.name.replace("_", " ").title(),
					"fieldtype": "Check",
					# TODO: insert after the last field. use meta to find the last field
					"insert_after": "additional_permissions",
					"depends_on": f"eval:doc.parent == '{self.applicable_for}'",
				},
			)

	def on_trash(self):
		if name := frappe.db.exists(
			"Custom DocPerm",
			{
				"fieldname": self.name,
				"reference_doctype": self.applicable_for,
			},
		):
			frappe.delete_doc("Custom DocPerm", name)
