import frappe


def execute():
	navbar_settings = frappe.get_single("Navbar Settings")
<<<<<<< HEAD
	duplicate_items = [
		navbar_item
		for navbar_item in navbar_settings.settings_dropdown
		if navbar_item.item_label == "Toggle Full Width"
	]
=======
	duplicate_items = []

	for navbar_item in navbar_settings.settings_dropdown:
		if navbar_item.item_label == "Toggle Full Width":
			duplicate_items.append(navbar_item)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	if len(duplicate_items) > 1:
		navbar_settings.remove(duplicate_items[0])
		navbar_settings.save()
