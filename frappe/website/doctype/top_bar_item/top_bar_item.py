# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class TopBarItem(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		label: DF.Data
		open_in_new_tab: DF.Check
		parent: DF.Data
		parent_label: DF.Literal[None]
		parentfield: DF.Data
		parenttype: DF.Data
		right: DF.Check
		url: DF.Data | None
	# end: auto-generated types

=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	pass
