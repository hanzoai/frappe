# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BackgroundTask(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		arguments: DF.JSON | None
		ended_at: DF.Datetime | None
		exception: DF.LongText | None
		method: DF.Data
		progress: DF.Percent
		queue: DF.Data | None
		ref_docname: DF.DynamicLink | None
		ref_doctype: DF.Link | None
		result: DF.LongText | None
		stage: DF.Data | None
		started_at: DF.Datetime | None
		status: DF.Literal["Queued", "Running", "Completed", "Failed"]
		task_id: DF.Data
		task_name: DF.Data
		user: DF.Link
	# end: auto-generated types

	pass
