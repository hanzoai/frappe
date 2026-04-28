import frappe
from frappe import format
<<<<<<< HEAD
from frappe.tests.utils import FrappeTestCase
from frappe.utils.formatters import format_value
=======
from frappe.tests import IntegrationTestCase
>>>>>>> 9bcac62d98 (fix(standard_macros): escape fields in standard print format template)


class TestFormatter(FrappeTestCase):
	def test_currency_formatting(self):
		df = frappe._dict({"fieldname": "amount", "fieldtype": "Currency", "options": "currency"})

		doc = frappe._dict({"amount": 5})
		frappe.db.set_default("currency", "INR")

		# if currency field is not passed then default currency should be used.
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "₹ 100,000.00")

		doc.currency = "USD"
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "$ 100,000.00")

		frappe.db.set_default("currency", None)
