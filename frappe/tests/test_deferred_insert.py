import frappe
from frappe.deferred_insert import deferred_insert, save_to_db
from frappe.tests.utils import FrappeTestCase


class TestDeferredInsert(FrappeTestCase):
	def test_deferred_insert(self):
		route_history = {"route": frappe.generate_hash(), "user": "Administrator"}
		deferred_insert("Route History", [route_history])

		save_to_db()
		self.assertTrue(frappe.db.exists("Route History", route_history))
<<<<<<< HEAD

		route_history = {"route": frappe.generate_hash(), "user": "Administrator"}
		deferred_insert("Route History", [route_history])
		frappe.clear_cache()  # deferred_insert cache keys are supposed to be persistent
		save_to_db()
		self.assertTrue(frappe.db.exists("Route History", route_history))
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
