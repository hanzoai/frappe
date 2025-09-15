# Copyright (c) 2017, Frappe Technologies and Contributors
# License: MIT. See LICENSE
import frappe
from frappe.tests import IntegrationTestCase


class TestSystemSettings(IntegrationTestCase):
	def test_db_decimal_precision_validation(self):
		"""Test validation of db_decimal_precision field"""
		system_settings = frappe.get_single("System Settings")
		
		# Test valid values
		valid_values = ["21,9", "18,6", "10,2", "5,0"]
		for valid_value in valid_values:
			system_settings.db_decimal_precision = valid_value
			try:
				system_settings.validate_db_decimal_precision()
			except Exception:
				self.fail(f"Valid value '{valid_value}' should not raise an exception")
		
		# Test invalid values
		invalid_values = ["abc,def", "21", "21,", ",9", "9,21", "66,10", "21,31", "0,5"]
		for invalid_value in invalid_values:
			system_settings.db_decimal_precision = invalid_value
			with self.assertRaises(frappe.ValidationError):
				system_settings.validate_db_decimal_precision()
	
	def test_db_decimal_precision_default(self):
		"""Test that db_decimal_precision returns correct default"""
		# Clear any existing value
		frappe.db.set_single_value("System Settings", "db_decimal_precision", "")
		frappe.db.commit()
		
		from frappe.database.schema import get_db_decimal_precision
		self.assertEqual(get_db_decimal_precision(), "21,9")
		
		# Set a custom value
		frappe.db.set_single_value("System Settings", "db_decimal_precision", "18,4")
		frappe.db.commit()
		
		self.assertEqual(get_db_decimal_precision(), "18,4")
		
		# Cleanup
		frappe.db.set_single_value("System Settings", "db_decimal_precision", "")
		frappe.db.commit()
	
	def test_schema_definition_with_custom_precision(self):
		"""Test that schema definition uses custom decimal precision"""
		from frappe.database.schema import get_definition
		
		# Set custom precision
		frappe.db.set_single_value("System Settings", "db_decimal_precision", "18,4")
		frappe.db.commit()
		
		# Test Float field with high precision
		result = get_definition("Float", precision=7)
		self.assertEqual(result, "decimal(18,4)")
		
		# Test Currency field with high precision
		result = get_definition("Currency", precision=8)
		self.assertEqual(result, "decimal(18,4)")
		
		# Test that low precision fields are unaffected
		result = get_definition("Float", precision=5)
		self.assertEqual(result, "decimal(18,6)")
		
		# Cleanup
		frappe.db.set_single_value("System Settings", "db_decimal_precision", "")
		frappe.db.commit()
