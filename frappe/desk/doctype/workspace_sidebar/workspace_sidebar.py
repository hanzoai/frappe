# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.desk.doctype.workspace.workspace import is_workspace_manager
from frappe.model.document import Document
from frappe.modules.export_file import delete_folder, export_to_files


class WorkspaceSidebar(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.desk.doctype.workspace_sidebar_item.workspace_sidebar_item import WorkspaceSidebarItem
		from frappe.types import DF

		items: DF.Table[WorkspaceSidebarItem]
		title: DF.Data | None
	# end: auto-generated types

	def on_update(self):
		if self.module and frappe.conf.developer_mode:
			export_to_files(record_list=[["Workspace Sidebar", self.name]], record_module=self.module)

	def on_trash(self):
		if not is_workspace_manager():
			frappe.throw(_("You need to be Workspace Manager to delete a public workspace."))

	def after_delete(self):
		if self.module and frappe.conf.developer_mode:
			delete_folder(self.module, "Workspace Sidebar", self.name)
