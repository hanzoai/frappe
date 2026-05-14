# Copyright (c) 2020, Frappe Technologies and contributors
# License: MIT. See LICENSE

from typing import TYPE_CHECKING

import frappe
from frappe import _
from frappe.model.document import Document

if TYPE_CHECKING:
	from frappe.core.doctype.docfield.docfield import DocField


class DocTypeLayout(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.core.doctype.doctype_layout_child_table.doctype_layout_child_table import (
			DocTypeLayoutChildTable,
		)
		from frappe.core.doctype.doctype_layout_field.doctype_layout_field import DocTypeLayoutField
		from frappe.types import DF

		based_on: DF.Link | None
		child_tables: DF.Table[DocTypeLayoutChildTable]
		condition: DF.Code | None
		default_email_template: DF.Link | None
		default_print_format: DF.Link | None
		document_type: DF.Link
		fields: DF.Table[DocTypeLayoutField]
		is_child_table: DF.Check
		is_standard: DF.Check
		module: DF.Link | None
		title: DF.Data
	# end: auto-generated types

	def on_update(self):
		if not frappe.flags.in_import and self.is_standard and frappe.conf.developer_mode:
			self._export_to_doctype_dir()

	def _export_to_doctype_dir(self):
		import os

		from frappe.modules.export_file import strip_default_fields
		from frappe.modules.utils import get_module_path

		module_path = get_module_path(self.module)
		folder = os.path.join(module_path, "doctype", frappe.scrub(self.document_type), "doctype_layout")
		frappe.create_folder(folder)

		doc_export = self.as_dict(no_nulls=True, ignore_computed_child_tables=True)
		self.run_method("before_export", doc_export)
		doc_export = strip_default_fields(self, doc_export)

		path = os.path.join(folder, f"{frappe.scrub(self.name)}.json")
		with open(path, "w+") as f:  # nosemgrep
			f.write(frappe.as_json(doc_export) + "\n")

	def after_insert(self):
		self.ensure_layout_link_field()

	def on_trash(self):
		self.cleanup_layout_link_field_if_unused()

	def validate(self):
		if self.is_standard and not frappe.conf.developer_mode and not frappe.flags.in_migrate:
			frappe.throw(
				_("Standard DocType Layouts can only be modified in developer mode."),
				frappe.PermissionError,
			)

		if self.based_on:
			parent_layout = frappe.db.get_value("DocType Layout", self.based_on, "document_type")
			if parent_layout != self.document_type:
				frappe.throw(
					_("Based On layout {0} must be for the same Document Type ({1})").format(
						frappe.bold(self.based_on), frappe.bold(self.document_type)
					)
				)

	@frappe.whitelist()
	def sync_fields(self):
		doctype_fields = frappe.get_meta(self.document_type, cached=False).fields

		if self.is_new():
			added_fields = [field.fieldname for field in doctype_fields]
			removed_fields = []
		else:
			doctype_fieldnames = {field.fieldname for field in doctype_fields}
			layout_fieldnames = {field.fieldname for field in self.fields}
			added_fields = list(doctype_fieldnames - layout_fieldnames)
			removed_fields = list(layout_fieldnames - doctype_fieldnames)

		if not (added_fields or removed_fields):
			return

		added = self.add_fields(added_fields, doctype_fields)
		removed = self.remove_fields(removed_fields)

		for index, field in enumerate(self.fields):
			field.idx = index + 1

		return {"added": added, "removed": removed}

	def ensure_layout_link_field(self):
		"""Add 'doctype_layout' custom Link field to target doctype if absent."""
		if frappe.get_meta(self.document_type).istable:
			return

		fieldname = "doctype_layout"
		if frappe.db.exists("Custom Field", {"dt": self.document_type, "fieldname": fieldname}):
			return

		frappe.get_doc(
			{
				"doctype": "Custom Field",
				"dt": self.document_type,
				"fieldname": fieldname,
				"label": "Layout",
				"fieldtype": "Link",
				"options": "DocType Layout",
				"read_only": 1,
				"no_copy": 1,
				"in_standard_filter": 1,
			}
		).insert(ignore_permissions=True)

	def cleanup_layout_link_field_if_unused(self):
		"""Remove 'doctype_layout' custom field if no layouts remain for this doctype."""
		remaining = frappe.db.count(
			"DocType Layout",
			{"document_type": self.document_type, "name": ["!=", self.name]},
		)
		if remaining:
			return

		custom_field = frappe.db.get_value(
			"Custom Field", {"dt": self.document_type, "fieldname": "doctype_layout"}
		)
		if custom_field:
			frappe.delete_doc("Custom Field", custom_field, ignore_permissions=True)

	def add_fields(self, added_fields: list[str], doctype_fields: list["DocField"]) -> list[dict]:
		added = []
		for field in added_fields:
			field_details = next((f for f in doctype_fields if f.fieldname == field), None)
			if not field_details:
				continue

			row = self.append(
				"fields",
				{
					"fieldname": field_details.fieldname,
					"label": field_details.label,
				},
			)
			row_data = row.as_dict()

			if field_details.get("insert_after"):
				insert_after = next(
					(f for f in self.fields if f.fieldname == field_details.insert_after),
					None,
				)
				if insert_after:
					self.fields.insert(insert_after.idx, row)
					self.fields.pop()
					row_data = {"idx": insert_after.idx + 1, "fieldname": row.fieldname, "label": row.label}

			added.append(row_data)
		return added

	def remove_fields(self, removed_fields: list[str]) -> list[dict]:
		removed = []
		for field in removed_fields:
			field_details = next((f for f in self.fields if f.fieldname == field), None)
			if field_details:
				self.remove(field_details)
				removed.append(field_details.as_dict())
		return removed


@frappe.whitelist()
def get_layouts_for_doctype(doctype: str) -> list[dict]:
	fields = [
		"name",
		"title",
		"document_type",
		"based_on",
		"is_standard",
		"default_print_format",
		"default_email_template",
	]
	return frappe.get_all(
		"DocType Layout",
		filters={"document_type": doctype},
		fields=fields,
		order_by="title asc",
	)
