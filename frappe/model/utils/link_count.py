# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe

ignore_doctypes = ("DocType", "Print Format", "Role", "Module Def", "Communication", "ToDo")


LINK_COUNT_BUFFER_SIZE = 256


def notify_link_count(doctype, name):
	"""updates link count for given document"""
	if hasattr(frappe.local, "link_count"):
		if (doctype, name) in frappe.local.link_count:
			frappe.local.link_count[(doctype, name)] += 1
		else:
			frappe.local.link_count[(doctype, name)] = 1


def flush_local_link_count():
	"""flush from local before ending request"""
	if not getattr(frappe.local, "link_count", None):
		return

	link_count = frappe.cache().get_value("_link_count")
	if not link_count:
		link_count = {}

	new_links = frappe.local.link_count
	flush = False
	for key, value in new_links.items():
		if key in link_count:
			link_count[key] += value
		elif len(link_count) < LINK_COUNT_BUFFER_SIZE:
			link_count[key] = value
		else:
			continue
		flush = True

	if flush:
		frappe.cache().set_value("_link_count", link_count)
	new_links.clear()


def update_link_count():
	"""increment link count in the `idx` column for the given document"""
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
