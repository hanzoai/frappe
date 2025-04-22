import frappe


def execute():
	frappe.model.delete_fields(
		{"Notification Settings": ["enable_email_energy_point", "energy_points_system_notifications"]},
		delete=1,
	)
