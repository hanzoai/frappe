# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

<<<<<<< HEAD
from collections import defaultdict

import frappe

ignore_doctypes = {
	"DocType",
	"Print Format",
	"Role",
	"Module Def",
	"Communication",
	"ToDo",
	"Version",
	"Error Log",
	"Scheduled Job Log",
	"Event Sync Log",
	"Event Update Log",
	"Access Log",
	"View Log",
	"Activity Log",
	"Energy Point Log",
	"Notification Log",
	"Email Queue",
	"DocShare",
	"Document Follow",
	"Console Log",
	"User",
}
=======
import frappe

ignore_doctypes = ("DocType", "Print Format", "Role", "Module Def", "Communication", "ToDo")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def notify_link_count(doctype, name):
	"""updates link count for given document"""
<<<<<<< HEAD

	if doctype in ignore_doctypes or not frappe.request:
		return

	if not hasattr(frappe.local, "_link_count"):
		frappe.local._link_count = defaultdict(int)
		frappe.db.after_commit.add(flush_local_link_count)

	frappe.local._link_count[(doctype, name)] += 1
=======
	if hasattr(frappe.local, "link_count"):
		if (doctype, name) in frappe.local.link_count:
			frappe.local.link_count[(doctype, name)] += 1
		else:
			frappe.local.link_count[(doctype, name)] = 1
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def flush_local_link_count():
	"""flush from local before ending request"""
<<<<<<< HEAD
	new_links = getattr(frappe.local, "_link_count", None)
	if not new_links:
		return

	link_count = frappe.cache.get_value("_link_count") or {}

	for key, value in new_links.items():
		if key in link_count:
			link_count[key] += value
		else:
			link_count[key] = value

	frappe.cache.set_value("_link_count", link_count)
	new_links.clear()
=======
	if not getattr(frappe.local, "link_count", None):
		return

	link_count = frappe.cache().get_value("_link_count")
	if not link_count:
		link_count = {}

		for key, _value in frappe.local.link_count.items():
			if key in link_count:
				link_count[key] += frappe.local.link_count[key]
			else:
				link_count[key] = frappe.local.link_count[key]

	frappe.cache().set_value("_link_count", link_count)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def update_link_count():
	"""increment link count in the `idx` column for the given document"""
<<<<<<< HEAD
	link_count = frappe.cache.get_value("_link_count")

	if link_count:
		for (doctype, name), count in link_count.items():
			try:
				table = frappe.qb.DocType(doctype)
				frappe.qb.update(table).set(table.idx, table.idx + count).where(table.name == name).run()
				frappe.db.commit()
			except Exception as e:
				if not frappe.db.is_table_missing(e):  # table not found, single
					raise e
	# reset the count
	frappe.cache.delete_value("_link_count")
=======
	link_count = frappe.cache().get_value("_link_count")

	if link_count:
		for key, count in link_count.items():
			if key[0] not in ignore_doctypes:
				try:
					frappe.db.sql(
						f"update `tab{key[0]}` set idx = idx + {count} where name=%s",
						key[1],
						auto_commit=1,
					)
				except Exception as e:
					if not frappe.db.is_table_missing(e):  # table not found, single
						raise e
	# reset the count
	frappe.cache().delete_value("_link_count")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
