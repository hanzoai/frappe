# Copyright (c) 2015, Frappe Technologies and Contributors
# License: MIT. See LICENSE
import frappe
<<<<<<< HEAD
from frappe.contacts.doctype.address_template.address_template import get_default_address_template
from frappe.tests.utils import FrappeTestCase
from frappe.utils.jinja import validate_template


class TestAddressTemplate(FrappeTestCase):
	def setUp(self) -> None:
		frappe.db.delete("Address Template", {"country": "India"})
		frappe.db.delete("Address Template", {"country": "Brazil"})

	def test_default_address_template(self):
		validate_template(get_default_address_template())

	def test_default_is_unset(self):
		frappe.get_doc({"doctype": "Address Template", "country": "India", "is_default": 1}).insert()

		self.assertEqual(frappe.db.get_value("Address Template", "India", "is_default"), 1)

		frappe.get_doc({"doctype": "Address Template", "country": "Brazil", "is_default": 1}).insert()

		self.assertEqual(frappe.db.get_value("Address Template", "India", "is_default"), 0)
		self.assertEqual(frappe.db.get_value("Address Template", "Brazil", "is_default"), 1)

	def test_delete_address_template(self):
		india = frappe.get_doc({"doctype": "Address Template", "country": "India", "is_default": 0}).insert()

		brazil = frappe.get_doc(
			{"doctype": "Address Template", "country": "Brazil", "is_default": 1}
		).insert()

		india.reload()  # might have been modified by the second template
		india.delete()  # should not raise an error

		self.assertRaises(frappe.ValidationError, brazil.delete)
=======
from frappe.tests.utils import FrappeTestCase


class TestAddressTemplate(FrappeTestCase):
	def setUp(self):
		self.make_default_address_template()

	def test_default_is_unset(self):
		a = frappe.get_doc("Address Template", "India")
		a.is_default = 1
		a.save()

		b = frappe.get_doc("Address Template", "Brazil")
		b.is_default = 1
		b.save()

		self.assertEqual(frappe.db.get_value("Address Template", "India", "is_default"), 0)

	def tearDown(self):
		a = frappe.get_doc("Address Template", "India")
		a.is_default = 1
		a.save()

	@classmethod
	def make_default_address_template(self):
		template = """{{ address_line1 }}<br>{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}{{ city }}<br>{% if state %}{{ state }}<br>{% endif -%}{% if pincode %}{{ pincode }}<br>{% endif -%}{{ country }}<br>{% if phone %}Phone: {{ phone }}<br>{% endif -%}{% if fax %}Fax: {{ fax }}<br>{% endif -%}{% if email_id %}Email: {{ email_id }}<br>{% endif -%}"""

		if not frappe.db.exists("Address Template", "India"):
			frappe.get_doc(
				{"doctype": "Address Template", "country": "India", "is_default": 1, "template": template}
			).insert()

		if not frappe.db.exists("Address Template", "Brazil"):
			frappe.get_doc(
				{"doctype": "Address Template", "country": "Brazil", "template": template}
			).insert()
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
