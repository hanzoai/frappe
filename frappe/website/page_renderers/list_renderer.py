import frappe
from frappe.modules import load_doctype_module
from frappe.website.page_renderers.template_page import TemplatePage


class ListPage(TemplatePage):
	def can_render(self):
		doctype = frappe.db.exists("DocType", self.path, True)
		if doctype and doctype != "Web Page":
			meta = frappe.get_meta(doctype)
			module = load_doctype_module(doctype)
			if meta.has_web_view or hasattr(module, "get_list_context"):
				return True
		return False

	def render(self):
		frappe.form_dict.doctype = self.path
		self.set_standard_path("portal")
		return super().render()
