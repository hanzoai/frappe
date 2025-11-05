# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import os
from json import JSONDecodeError, dumps, loads

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.modules.utils import create_directory_on_app_path


class WorkspaceSidebar(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.desk.doctype.workspace_sidebar_item.workspace_sidebar_item import WorkspaceSidebarItem
		from frappe.types import DF

		app: DF.Autocomplete | None
		items: DF.Table[WorkspaceSidebarItem]
		title: DF.Data | None
	# end: auto-generated types

	def on_update(self):
		if frappe.conf.developer_mode:
			if self.app:
				self.export_sidebar()

	def export_sidebar(self):
		folder_path = create_directory_on_app_path("workspace_sidebar", self.app)
		file_path = os.path.join(folder_path, f"{frappe.scrub(self.title)}.json")
		doc_export = self.as_dict(no_nulls=True, no_private_properties=True)
		with open(file_path, "w+") as doc_file:
			doc_file.write(frappe.as_json(doc_export) + "\n")

	def delete_file(self):
		folder_path = create_directory_on_app_path("workspace_sidebar", self.app)
		file_path = os.path.join(folder_path, f"{frappe.scrub(self.title)}.json")
		if not os.path.exists(file_path):
			os.remove(file_path)

	def on_trash(self):
		if is_workspace_manager():
			if frappe.conf.developer_mode and self.app:
				self.file()
		else:
			frappe.throw(_("You need to be Workspace Manager to delete a public workspace."))


def is_workspace_manager():
	return "Workspace Manager" in frappe.get_roles()


def create_workspace_sidebar_for_workspaces():
	from frappe.query_builder import DocType

	workspace = DocType("Workspace")

	all_workspaces = (
		frappe.qb.from_(workspace)
		.select(workspace.name)
		.where((workspace.public == 1) & (workspace.name != "Welcome Workspace"))
	).run(pluck=True)

	existing_sidebars = frappe.get_all("Workspace Sidebar", pluck="title")
	for workspace in all_workspaces:
		if workspace not in existing_sidebars:
			sidebar = frappe.new_doc("Workspace Sidebar")
			sidebar.title = workspace
			sidebar.header_icon = frappe.db.get_value("Workspace", workspace, "icon")
			sidebar.save()


@frappe.whitelist()
def add_sidebar_items(sidebar_title, sidebar_items):
	sidebar_items = loads(sidebar_items)
	w = frappe.get_doc("Workspace Sidebar", sidebar_title)
	items = []
	current_idx = 1
	for item in sidebar_items:
		si = frappe.new_doc("Workspace Sidebar Item")
		si.update(item)
		items.append(si)
		si.idx = current_idx
		items.append(si)
		current_idx += 1

		nested_items = item.get("nested_items", [])
		if nested_items:
			for nested_item in nested_items:
				new_nested_item = frappe.new_doc("Workspace Sidebar Item")
				new_nested_item.update(nested_item)
				new_nested_item.child = 1
				new_nested_item.idx = current_idx
				items.append(new_nested_item)
				current_idx += 1

	w.items = items
	w.save()
	return w


def add_to_my_workspace(workspace):
	private_sidebar = frappe.get_doc("Workspace Sidebar", "My Workspaces")

	workspace_sidebar = {
		"label": workspace.title,
		"type": "Link",
		"link_to": f"{workspace.title}-{workspace.for_user}",
		"link_type": "Workspace",
		"icon": workspace.icon,
	}

	private_sidebar.append("items", workspace_sidebar)

	private_sidebar.save()
