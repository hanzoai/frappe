# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class WebsiteSidebar(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from frappe.website.doctype.website_sidebar_item.website_sidebar_item import WebsiteSidebarItem

		sidebar_items: DF.Table[WebsiteSidebarItem]
		title: DF.Data

	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	def get_items(self):
		items = frappe.get_all(
			"Website Sidebar Item",
			filters={"parent": self.name},
			fields=["title", "route", "group"],
			order_by="idx asc",
		)

		items_by_group = {}
		items_without_group = []
		for item in items:
			if item.group:
				items_by_group.setdefault(item.group, []).append(item)
			else:
				items_without_group.append(item)

<<<<<<< HEAD
		out = [{"group_title": group, "group_items": items} for group, items in items_by_group.items()]
=======
		out = []
		for group, items in items_by_group.items():
			out.append({"group_title": group, "group_items": items})

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		out += items_without_group
		return out
