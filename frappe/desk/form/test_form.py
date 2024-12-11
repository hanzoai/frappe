# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from frappe.tests.utils import FrappeTestCase


class TestForm(FrappeTestCase):
	def test_linked_with(self):
		results = get_linked_docs("Role", "System Manager", linkinfo=get_linked_doctypes("Role"))
		self.assertTrue("User" in results)
		self.assertTrue("DocType" in results)
<<<<<<< HEAD
=======


if __name__ == "__main__":
	import unittest

	frappe.connect()
	unittest.main()
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
