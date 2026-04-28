# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

<<<<<<< HEAD
# import frappe
from frappe.tests.utils import FrappeTestCase


class TestDiscussionTopic(FrappeTestCase):
	pass
=======
import frappe
from frappe.tests import IntegrationTestCase
from frappe.website.doctype.discussion_topic.discussion_topic import submit_discussion


class TestDiscussionTopic(IntegrationTestCase):
	def test_edit_discussion_reply(self):
		"""Test whether editing a reply is restricted to the owner."""
		topic_name = submit_discussion("User", "Administrator", "Original", "Title")
		reply_name = frappe.db.get_value("Discussion Reply", {"topic": topic_name}, "name")

		frappe.set_user("Guest")
		with self.assertRaises(frappe.PermissionError):
			submit_discussion("User", "Administrator", "Hacked", "Title", reply_name=reply_name)

		self.assertEqual(frappe.db.get_value("Discussion Reply", reply_name, "reply"), "Original")

		frappe.set_user("Administrator")
		submit_discussion("User", "Administrator", "Changed!", "Title", reply_name=reply_name)
		self.assertEqual(frappe.db.get_value("Discussion Reply", reply_name, "reply"), "Changed!")
>>>>>>> a9d98723b4 (test: add test to check if reply is restricted to owner)
