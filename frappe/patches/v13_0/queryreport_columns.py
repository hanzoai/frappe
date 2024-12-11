# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import frappe


def execute():
	"""Convert Query Report json to support other content"""
	records = frappe.get_all("Report", filters={"json": ["!=", ""]}, fields=["name", "json"])
	for record in records:
		jstr = record["json"]
		data = json.loads(jstr)
		if isinstance(data, list):
			# double escape braces
			jstr = f'{{"columns":{jstr}}}'
<<<<<<< HEAD
			frappe.db.set_value("Report", record["name"], "json", jstr)
=======
			frappe.db.update("Report", record["name"], "json", jstr)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
