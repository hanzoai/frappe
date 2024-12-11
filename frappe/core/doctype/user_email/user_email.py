# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE

from frappe.model.document import Document


class UserEmail(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		awaiting_password: DF.Check
		email_account: DF.Link
		email_id: DF.Data | None
		enable_outgoing: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		used_oauth: DF.Check
	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	pass
