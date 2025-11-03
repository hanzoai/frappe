# Copyright (c) 2025, Frappe Technologies and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestPermissionType(IntegrationTestCase):
	"""
	Integration tests for PermissionType.
	Use this class for testing interactions between multiple components.
	"""

	def test_permission_type_creation_deletion(self): ...

	def test_permission_type_creation_reserved_name(self): ...

	def test_role_permission_with_custom_permission_type(self): ...

	def test_share_permission_with_custom_permission_type(self): ...

	def test_role_permission_mapping_with_custom_permission_type(self): ...

	def test_export_import_of_permission_type(self): ...
