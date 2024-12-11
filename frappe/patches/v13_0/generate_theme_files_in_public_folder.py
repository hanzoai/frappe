# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe


def execute():
	frappe.reload_doc("website", "doctype", "website_theme_ignore_app")
	themes = frappe.get_all("Website Theme", filters={"theme_url": ("not like", "/files/website_theme/%")})
	for theme in themes:
		doc = frappe.get_doc("Website Theme", theme.name)
		try:
<<<<<<< HEAD
=======
			doc.generate_bootstrap_theme()
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			doc.save()
		except Exception:
			print("Ignoring....")
			print(frappe.get_traceback())
