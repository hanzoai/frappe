# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class WorkflowTransition(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Link
		allow_self_approval: DF.Check
		allowed: DF.Link
		condition: DF.Code | None
		next_state: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		state: DF.Link
	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	pass
