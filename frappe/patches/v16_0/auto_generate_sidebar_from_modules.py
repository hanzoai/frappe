import frappe


def execute():
	"""Auto generate sidebar from module"""
	sidebars = []
	for module in frappe.get_all("Module Def", pluck="name"):
		if not (
			frappe.db.exists("Workspace Sidebar", {"module": module})
			or frappe.db.exists("Workspace Sidebar", {"name": module})
		):
			print("Fetching information for Module", module)
			module_info = get_module_info(module)
			sidebar_items = create_sidebar_items(module_info)
			sidebar = frappe.new_doc("Workspace Sidebar")
			sidebar.title = module
			sidebar.items = sidebar_items
			sidebar.header_icon = "hammer"
			sidebars.append(sidebar)
			sidebar.save()
	return sidebars


def get_module_info(module_name):
	entities = ["Workspace", "Dashboard", "DocType", "Report", "Page"]
	module_info = {}

	for entity in entities:
		module_info[entity] = {}
		filters = [{"module": module_name}]
		if entity.lower() == "doctype":
			filters.append({"istable": 0})
		module_info[entity] = frappe.get_all(entity, filters=filters, pluck="name")

	return module_info


def create_sidebar_items(module_info):
	sidebar_items = []
	for entity, items in module_info.items():
		if entity.lower() == "report":
			section_break = frappe.new_doc("Workspace Sidebar Item")
			section_break.update(
				{
					"type": "Section Break",
				}
			)
			sidebar_items.append(section_break)
		for item in items:
			item_info = {"label": item, "type": "Link", "link_type": entity, "link_to": item}
			if entity.lower() == "workspace":
				item_info["icon"] = "home"

			if entity.lower() == "doctype" and "settings" in item.lower():
				item_info["icon"] = "settings"

			sidebar_item = frappe.new_doc("Workspace Sidebar Item")
			sidebar_item.update(item_info)
			sidebar_items.append(sidebar_item)

	return sidebar_items
