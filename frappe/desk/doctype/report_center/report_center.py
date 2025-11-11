# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import os

import frappe
from frappe.model.document import Document
from frappe.modules.utils import create_directory_on_app_path, get_app_level_directory_path


class ReportCenter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.desk.doctype.report_center_link.report_center_link import ReportCenterLink
		from frappe.types import DF

		app: DF.Autocomplete | None
		links: DF.Table[ReportCenterLink]
		sidebar: DF.Link | None
	# end: auto-generated types

	def on_update(self):
		if frappe.conf.developer_mode:
			if self.app:
				self.export_report_center()

	def export_report_center(self):
		folder_path = create_directory_on_app_path("report_center", self.app)
		file_path = os.path.join(folder_path, f"{frappe.scrub(self.name)}.json")
		doc_export = self.as_dict(no_nulls=True, no_private_properties=True)
		with open(file_path, "w+") as doc_file:
			doc_file.write(frappe.as_json(doc_export) + "\n")

	def on_trash(self):
		if frappe.conf.developer_mode and self.app:
			self.delete_file()

	def delete_file(self):
		folder_path = create_directory_on_app_path("report_center", self.app)
		file_path = os.path.join(folder_path, f"{frappe.scrub(self.name)}.json")
		if os.path.exists(file_path):
			os.remove(file_path)
