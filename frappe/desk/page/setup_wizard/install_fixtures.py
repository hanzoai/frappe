# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.desk.doctype.global_search_settings.global_search_settings import (
	update_global_search_doctypes,
)
from frappe.utils.dashboard import sync_dashboards


<<<<<<< HEAD
def _(x, *args, **kwargs):
	"""Redefine the translation function to return the string as is.
	We want to create english records but still mark the strings as translatable.
	The respective DocTypes have 'Translate Link Fields' enabled."""
	return x


=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
def install():
	update_genders()
	update_salutations()
	update_global_search_doctypes()
	setup_email_linking()
	sync_dashboards()
	add_unsubscribe()


<<<<<<< HEAD
def update_genders():
	for gender in (
		_("Male"),
		_("Female"),
		_("Other"),
		_("Transgender"),
		_("Genderqueer"),
		_("Non-Conforming"),
		_("Prefer not to say"),
	):
		doc = frappe.new_doc("Gender")
		doc.gender = gender
		doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def update_salutations():
	for salutation in (
		_("Mr"),
		_("Ms"),
		_("Mx"),
		_("Dr"),
		_("Mrs"),
		_("Madam"),
		_("Miss"),
		_("Master"),
		_("Prof"),
	):
		doc = frappe.new_doc("Salutation")
		doc.salutation = salutation
=======
@frappe.whitelist()
def update_genders():
	default_genders = [
		"Male",
		"Female",
		"Other",
		"Transgender",
		"Genderqueer",
		"Non-Conforming",
		"Prefer not to say",
	]
	records = [{"doctype": "Gender", "gender": d} for d in default_genders]
	for record in records:
		frappe.get_doc(record).insert(ignore_permissions=True, ignore_if_duplicate=True)


@frappe.whitelist()
def update_salutations():
	default_salutations = ["Mr", "Ms", "Mx", "Dr", "Mrs", "Madam", "Miss", "Master", "Prof"]
	records = [{"doctype": "Salutation", "salutation": d} for d in default_salutations]
	for record in records:
		doc = frappe.new_doc(record.get("doctype"))
		doc.update(record)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def setup_email_linking():
<<<<<<< HEAD
	doc = frappe.new_doc("Email Account")
	doc.email_id = "email_linking@example.com"
=======
	doc = frappe.get_doc(
		{
			"doctype": "Email Account",
			"email_id": "email_linking@example.com",
		}
	)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


def add_unsubscribe():
<<<<<<< HEAD
	for unsubscribe in [
		{"email": "admin@example.com", "global_unsubscribe": 1},
		{"email": "guest@example.com", "global_unsubscribe": 1},
	]:
=======
	email_unsubscribe = [
		{"email": "admin@example.com", "global_unsubscribe": 1},
		{"email": "guest@example.com", "global_unsubscribe": 1},
	]

	for unsubscribe in email_unsubscribe:
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		if not frappe.get_all("Email Unsubscribe", filters=unsubscribe):
			doc = frappe.new_doc("Email Unsubscribe")
			doc.update(unsubscribe)
			doc.insert(ignore_permissions=True)
