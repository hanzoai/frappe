# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

from collections import defaultdict

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.modules.export_file import delete_folder
from frappe.modules.utils import get_doctype_module
from frappe.utils.caching import site_cache

# doctypes where custom fields for permission types will be created
CUSTOM_FIELD_TARGET = ["Custom DocPerm", "DocPerm", "DocShare"]


class PermissionType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicable_for: DF.Link
		label: DF.Data | None
	# end: auto-generated types

	def validate(self):
		from frappe.permissions import rights

		if self.name in rights:
			frappe.throw(
				_("Permission Type '{0}' is reserved. Please choose another name.").format(self.name)
			)

	def _can_write(self):
		return (
			frappe.conf.developer_mode
			or frappe.flags.in_migrate
			or frappe.flags.in_install
		)

	def on_update(self):
		if not self._can_write():
			frappe.throw(_("Creation of this document is only permitted in developer mode."))

		from frappe.modules.export_file import export_to_files

		module = get_doctype_module(self.applicable_for)
		export_to_files(record_list=[["Permission Type", self.name]], record_module=module)

		for doctype in CUSTOM_FIELD_TARGET:
			self.create_custom_field(doctype)

	def create_custom_field(self, doctype):
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field

		if not self.custom_field_exists(doctype):
			depends_on = f"eval:doc.parent == '{self.applicable_for}'"
			if doctype == "DocShare":
				depends_on = f"eval:doc.share_doctype == '{self.applicable_for}'"

			create_custom_field(
				doctype,
				{
					"fieldname": self.name,
					"label": self.name.replace("_", " ").title(),
					"fieldtype": "Check",
					"insert_after": "append",
					"depends_on": depends_on,
				},
			)

	def on_trash(self):
		if not self._can_write():
			frappe.throw(_("Deletion of this document is only permitted in developer mode."))

		for doctype in CUSTOM_FIELD_TARGET:
			self.delete_custom_field(doctype)

		module = get_doctype_module(self.applicable_for)
		delete_folder(module, "Permission Type", self.name)

	def delete_custom_field(self, doctype):
		if name := self.custom_field_exists(doctype):
			frappe.delete_doc("Custom Field", name)

	def custom_field_exists(self, doctype):
		return frappe.db.exists(
			"Custom Field",
			{
				"fieldname": self.name,
				"dt": doctype,
			},
		)


@site_cache
def get_custom_ptype_map():
	ptypes = frappe.get_all(
		"Permission Type",
		fields=["name", "label", "applicable_for"],
		order_by="name",
	)
	custom_ptype_map = defaultdict(list)
	for pt in ptypes:
		custom_ptype_map[pt["applicable_for"]].append(pt["label"] or pt["name"])
	return dict(custom_ptype_map)
