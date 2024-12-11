import frappe
from frappe.desk.doctype.workspace.workspace import update_page
from frappe.utils import strip_html
from frappe.utils.html_utils import unescape_html


def execute():
	workspaces_to_update = frappe.get_all(
		"Workspace",
		filters={"module": ("is", "not set")},
<<<<<<< HEAD
		fields=["name", "title", "icon", "indicator_color", "parent_page as parent", "public"],
=======
		fields=["name", "title", "icon", "parent_page as parent", "public"],
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	)
	for workspace in workspaces_to_update:
		new_title = strip_html(unescape_html(workspace.title))

		if new_title == workspace.title:
			continue

		workspace.title = new_title
		try:
			update_page(**workspace)
			frappe.db.commit()

		except Exception:
			frappe.db.rollback()
