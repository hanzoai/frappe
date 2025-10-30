# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.modules.export_file import delete_folder
from frappe.modules.utils import get_doctype_module


class PermissionType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicable_for: DF.Link
		label: DF.Data | None
	# end: auto-generated types

	def on_update(self):
		if not frappe.conf.developer_mode and not frappe.flags.in_migrate:
			frappe.throw(_("Creation of this document is only permitted in developer mode."))

		from frappe.modules.export_file import export_to_files

		module = get_doctype_module(self.applicable_for)
		export_to_files(record_list=[["Permission Type", self.name]], record_module=module)

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
		if not frappe.conf.developer_mode and not frappe.flags.in_migrate:
			frappe.throw(_("Deletion of this document is only permitted in developer mode."))

		for doctype in ["Custom DocPerm", "DocPerm"]:
			self.delete_custom_docperm(doctype)

		module = get_doctype_module(self.applicable_for)
		delete_folder(module, "Permission Type", self.name)

	def delete_custom_docperm(self, doctype):
		if name := frappe.db.exists(
			"Custom Field",
			{
				"fieldname": self.name,
				"dt": doctype,
			},
		):
			frappe.delete_doc("Custom Field", name)
