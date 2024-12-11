# Copyright (c) 2017, Frappe Technologies and contributors
# License: MIT. See LICENSE

from frappe.model.document import Document


class Salutation(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		salutation: DF.Data | None
	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	pass
