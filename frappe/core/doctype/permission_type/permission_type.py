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
		from frappe.core.doctype.permission_type_doctype.permission_type_doctype import PermissionTypeDocType
		from frappe.types import DF

		doc_types: DF.TableMultiSelect[PermissionTypeDocType]
		module: DF.Link
	# end: auto-generated types

	def before_insert(self):
		self.name = frappe.scrub(self.name)

	def validate(self):
		from frappe.permissions import std_rights

		if self.name in std_rights:
			frappe.throw(
				_("Permission Type '{0}' is reserved. Please choose another name.").format(self.name)
			)

	def can_write(self):
		return frappe.conf.developer_mode or frappe.flags.in_migrate or frappe.flags.in_install

	def on_update(self):
		if not self.can_write():
			frappe.throw(_("Creation of this document is only permitted in developer mode."))

		from frappe.modules.export_file import export_to_files

		export_to_files(record_list=[["Permission Type", self.name]], record_module=self.module)

		for target in CUSTOM_FIELD_TARGET:
			self.create_custom_field(target)

	def create_custom_field(self, target):
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field

		if not self.custom_field_exists(target):
			field = "share_doctype" if target == "DocShare" else "parent"
			doc_types = [dt.doc_type for dt in self.doc_types if dt.doc_type]
			depends_on = f"eval:{frappe.as_json(doc_types)}.includes(doc.{field})"

			create_custom_field(
				target,
				{
					"fieldname": self.name,
					"label": self.name.replace("_", " ").title(),
					"fieldtype": "Check",
					"insert_after": "append",
					"depends_on": depends_on,
				},
			)

	def on_trash(self):
		if not self.can_write():
			frappe.throw(_("Deletion of this document is only permitted in developer mode."))

		for target in CUSTOM_FIELD_TARGET:
			self.delete_custom_field(target)

		delete_folder(self.module, "Permission Type", self.name)

	def delete_custom_field(self, target):
		if name := self.custom_field_exists(target):
			frappe.delete_doc("Custom Field", name)

	def custom_field_exists(self, target):
		return frappe.db.exists(
			"Custom Field",
			{
				"fieldname": self.name,
				"dt": target,
			},
		)


@site_cache
def get_doctype_ptype_map():
	ptypes = frappe.qb.get_query(
		"Permission Type",
		fields=[
			"name",
			{"doc_types": ["doc_type"]},
		],
		order_by="name",
	)
	ptypes = ptypes.run(as_dict=True)

	doctype_ptype_map = defaultdict(list)
	for pt in ptypes:
		for dt in pt.doc_types:
			if pt.name not in doctype_ptype_map[dt.doc_type]:
				doctype_ptype_map[dt.doc_type].append(pt.name)
	return dict(doctype_ptype_map)
