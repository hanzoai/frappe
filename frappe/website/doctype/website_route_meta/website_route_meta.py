# Copyright (c) 2019, Frappe Technologies and contributors
# License: MIT. See LICENSE

from frappe.model.document import Document


class WebsiteRouteMeta(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from frappe.website.doctype.website_meta_tag.website_meta_tag import WebsiteMetaTag

		meta_tags: DF.Table[WebsiteMetaTag]

	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	def autoname(self):
		if self.name and self.name.startswith("/"):
			self.name = self.name[1:]
