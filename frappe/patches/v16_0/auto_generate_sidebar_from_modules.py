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


def get_module_info(module_name):
	entities = ["Workspace", "Dashboard", "DocType", "Report", "Page"]
	module_info = {}

	for entity in entities:
		module_info[entity] = {}
		filters = [{"module": module_name}]
		if entity.lower() == "doctype":
			filters.append({"istable": 0})
		module_info[entity] = frappe.get_all(entity, filters=filters, pluck="name")

	# if module info has no workspaces, then move doctypes to the front
	if not module_info.get("Workspace"):
		module_info = {
			"DocType": module_info.get("DocType"),
			"Workspace": module_info.get("Workspace"),
			"Report": module_info.get("Report"),
			"Dashboard": module_info.get("Dashboard"),
			"Page": module_info.get("Page"),
		}
	return module_info


def create_sidebar_items(module_info):
	sidebar_items = []
	idx = 1

	section_entities = {"report": "Reports", "dashboard": "Dashboards", "page": "Pages"}

	for entity, items in module_info.items():
		section_break_added = False
		entity_lower = entity.lower()

		if entity_lower in section_entities:
			if entity_lower == "report":
				section_break = add_section_breaks("Reports", idx)
			elif entity_lower in ("dashboard", "page") and len(items) > 1:
				section_break = add_section_breaks(section_entities[entity_lower], idx)
				section_break_added = True
			sidebar_items.append(section_break)
			idx += 1

		for item in items:
			print(entity, item)
			item_info = {"label": item, "type": "Link", "link_type": entity, "link_to": item, "idx": idx}

			if entity_lower == "report":
				item_info["child"] = 1

			if entity_lower == "workspace":
				item_info["icon"] = "home"

			if entity_lower == "doctype" and "settings" in item.lower():
				item_info["icon"] = "settings"

			if section_break_added:
				item_info["child"] = 1

			sidebar_item = frappe.new_doc("Workspace Sidebar Item")
			sidebar_item.update(item_info)
			sidebar_items.append(sidebar_item)

			idx += 1

	return sidebar_items


def add_section_breaks(label, idx):
	section_break = frappe.new_doc("Workspace Sidebar Item")
	section_break.update({"label": label, "type": "Section Break", "idx": idx})
	return section_break
