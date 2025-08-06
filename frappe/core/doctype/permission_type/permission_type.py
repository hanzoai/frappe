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
		doctypes = ["Custom DocPerm", "DocPerm"]
		for doctype in doctypes:
			self.create_custom_docperm(doctype)

	def create_custom_docperm(self, doctype):
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field

		if not frappe.db.exists(
			doctype,
			{
				"fieldname": self.name,
				"parent": self.applicable_for,
			},
		):
			create_custom_field(
				doctype,
				{
					"fieldname": self.name,
					"label": self.name.replace("_", " ").title(),
					"fieldtype": "Check",
					"insert_after": "append",
					"depends_on": f"eval:doc.parent == '{self.applicable_for}'",
				},
			)

	def on_trash(self):
		for doctype in ["Custom DocPerm", "DocPerm"]:
			self.delete_custom_docperm(doctype)

	def delete_custom_docperm(self, doctype):
		if name := frappe.db.exists(
			"Custom Field",
			{
				"fieldname": self.name,
				"dt": doctype,
			},
		):
			frappe.delete_doc("Custom Field", name)
