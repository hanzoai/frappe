# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.model.document import Document
<<<<<<< HEAD
=======
from frappe.utils import cint
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
from frappe.utils.jinja import validate_template


class AddressTemplate(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		country: DF.Link
		is_default: DF.Check
		template: DF.Code | None

	# end: auto-generated types
	def validate(self):
		validate_template(self.template)

		if not self.template:
			self.template = get_default_address_template()

		if not self.is_default and not self._get_previous_default():
			self.is_default = 1
			if frappe.db.get_single_value("System Settings", "setup_complete"):
				frappe.msgprint(_("Setting this Address Template as default as there is no other default"))

	def on_update(self):
		if self.is_default and (previous_default := self._get_previous_default()):
			frappe.db.set_value("Address Template", previous_default, "is_default", 0)
=======
	def validate(self):
		if not self.template:
			self.template = get_default_address_template()

		self.defaults = frappe.db.get_values("Address Template", {"is_default": 1, "name": ("!=", self.name)})
		if not self.is_default:
			if not self.defaults:
				self.is_default = 1
				if cint(frappe.db.get_single_value("System Settings", "setup_complete")):
					frappe.msgprint(
						_("Setting this Address Template as default as there is no other default")
					)

		validate_template(self.template)

	def on_update(self):
		if self.is_default and self.defaults:
			for d in self.defaults:
				frappe.db.set_value("Address Template", d[0], "is_default", 0)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	def on_trash(self):
		if self.is_default:
			frappe.throw(_("Default Address Template cannot be deleted"))

<<<<<<< HEAD
	def _get_previous_default(self) -> str | None:
		return frappe.db.get_value("Address Template", {"is_default": 1, "name": ("!=", self.name)})


@frappe.whitelist()
def get_default_address_template() -> str:
	"""Return the default address template."""
	from pathlib import Path

	return (Path(__file__).parent / "address_template.jinja").read_text()
=======

@frappe.whitelist()
def get_default_address_template():
	"""Get default address template (translated)"""
	return (
		"""{{ address_line1 }}<br>{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}\
{{ city }}<br>
{% if state %}{{ state }}<br>{% endif -%}
{% if pincode %}{{ pincode }}<br>{% endif -%}
{{ country }}<br>
{% if phone %}"""
		+ _("Phone")
		+ """: {{ phone }}<br>{% endif -%}
{% if fax %}"""
		+ _("Fax")
		+ """: {{ fax }}<br>{% endif -%}
{% if email_id %}"""
		+ _("Email")
		+ """: {{ email_id }}<br>{% endif -%}"""
	)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
