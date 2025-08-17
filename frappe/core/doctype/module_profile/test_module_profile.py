# Copyright (c) 2020, Frappe Technologies and Contributors
# License: MIT. See LICENSE
import frappe
from frappe.tests.utils import FrappeTestCase


<<<<<<< HEAD
class TestModuleProfile(FrappeTestCase):
=======
class TestModuleProfile(IntegrationTestCase):
	def setUp(self):
		# Clean slate before each test
		frappe.delete_doc_if_exists("Module Profile", "_Test Module Profile", force=1)
		frappe.delete_doc_if_exists("Module Profile", "_Test Module Profile 2", force=1)
		frappe.delete_doc_if_exists("User", "test-module-user1@example.com", force=1)
		frappe.delete_doc_if_exists("User", "test-module-user2@example.com", force=1)

>>>>>>> 8d04ecba9e (ci: add unit tests)
	def test_make_new_module_profile(self):
		if not frappe.db.get_value("Module Profile", "_Test Module Profile"):
			frappe.get_doc(
				{
					"doctype": "Module Profile",
					"module_profile_name": "_Test Module Profile",
					"block_modules": [{"module": "Accounts"}],
				}
			).insert()

		# add to user and check
		if not frappe.db.get_value("User", "test-for-module_profile@example.com"):
			new_user = frappe.get_doc(
				{"doctype": "User", "email": "test-for-module_profile@example.com", "first_name": "Test User"}
			).insert()
		else:
			new_user = frappe.get_doc("User", "test-for-module_profile@example.com")

		new_user.module_profile = "_Test Module Profile"
		new_user.save()

		self.assertEqual(new_user.block_modules[0].module, "Accounts")

	def test_multiple_block_modules(self):
		"""Assign multiple blocked modules from profile to user"""
		module_profile = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile",
				"block_modules": [{"module": "Accounts"}, {"module": "CRM"}, {"module": "HR"}],
			}
		).insert()

		user = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user1@example.com", "first_name": "Test User"}
		).insert()

		user.module_profile = module_profile.name
		user.save()

		self.assertSetEqual({bm.module for bm in user.block_modules}, {"Accounts", "CRM", "HR"})

	def test_update_module_profile_propagates_to_users(self):
		"""Updating block_modules in profile should update linked users"""
		module_profile = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile",
				"block_modules": [{"module": "Accounts"}],
			}
		).insert()

		user = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user1@example.com", "first_name": "Test User"}
		).insert()

		user.module_profile = module_profile.name
		user.save()

		self.assertEqual({bm.module for bm in user.block_modules}, {"Accounts"})

		# Update module profile

		module_profile.append("block_modules", {"module": "Projects"})
		module_profile.save()

		user.reload()
		self.assertSetEqual({bm.module for bm in user.block_modules}, {"Accounts", "Projects"})

	def test_clear_block_modules(self):
		"""Clearing block_modules in profile should also clear them for users"""
		module_profile = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile",
				"block_modules": [{"module": "Accounts"}],
			}
		).insert()

		user = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user1@example.com", "first_name": "Test User"}
		).insert()

		user.module_profile = module_profile.name
		user.save()
		self.assertTrue(user.block_modules)

		# Clear profile modules
		module_profile.block_modules = []
		module_profile.save()

		user.reload()
		self.assertEqual(user.block_modules, [])

	def test_multiple_users_same_profile(self):
		"""Updates should propagate to all users linked to the same profile"""
		module_profile = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile",
				"block_modules": [{"module": "Accounts"}],
			}
		).insert()

		user1 = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user1@example.com", "first_name": "User One"}
		).insert()
		user2 = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user2@example.com", "first_name": "User Two"}
		).insert()

		for u in (user1, user2):
			u.module_profile = module_profile.name
			u.save()

		# Update profile
		module_profile.append("block_modules", {"module": "Projects"})
		module_profile.save()

		user1.reload()
		user2.reload()
		self.assertEqual([bm.module for bm in user1.block_modules], ["Accounts", "Projects"])
		self.assertEqual([bm.module for bm in user2.block_modules], ["Accounts", "Projects"])

	def test_switch_user_module_profile(self):
		"""Switching user to a different profile updates their block_modules"""
		profile1 = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile",
				"block_modules": [{"module": "Accounts"}],
			}
		).insert()
		profile2 = frappe.get_doc(
			{
				"doctype": "Module Profile",
				"module_profile_name": "_Test Module Profile 2",
				"block_modules": [{"module": "HR"}],
			}
		).insert()

		user = frappe.get_doc(
			{"doctype": "User", "email": "test-module-user1@example.com", "first_name": "Test User"}
		).insert()

		user.module_profile = profile1.name
		user.save()
		self.assertEqual([bm.module for bm in user.block_modules], ["Accounts"])

		# Switch to another profile
		user.module_profile = profile2.name
		user.save()
		self.assertEqual([bm.module for bm in user.block_modules], ["HR"])
