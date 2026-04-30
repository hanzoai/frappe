# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import time
from collections.abc import Callable

import frappe
from frappe.model.document import Document

PUBLISH_THROTTLE_SECONDS = 0.2


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
		show_progress_bar: DF.Check
		stage: DF.Data | None
		started_at: DF.Datetime | None
		status: DF.Literal["Queued", "Running", "Completed", "Failed", "Cancelled"]
		task_id: DF.Data
		job_id: DF.Data | None
		task_name: DF.Data
		user: DF.Link
	# end: auto-generated types

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._last_published: float = 0.0

	def after_insert(self):
		frappe.publish_realtime(
			event="task_update",
			message={"task_id": self.task_id, "task_name": self.task_name, "status": "Queued"},
			user=self.user,
			after_commit=True,
		)

	def update_stage(self, stage: str) -> None:
		"""Publish a stage description without numeric progress"""
		self._publish({"task_id": self.task_id, "task_name": self.task_name, "stage": stage})

	def publish_progress(self, percent: int | float, stage: str | None = None) -> None:
		"""Publish numeric progress (0-100)"""
		now = time.monotonic()
		if percent < 100 and (now - self._last_published) < PUBLISH_THROTTLE_SECONDS:
			return
		self._last_published = now

		message: dict = {"task_id": self.task_id, "task_name": self.task_name, "progress": percent}
		if stage:
			message["stage"] = stage
		self._publish(message)

	def store_result(self, result) -> None:
		"""Store a JSON result of the task in DB"""
		self.db_set("result", frappe.as_json(result))

	def attach_file(
		self,
		file_name: str,
		content: bytes,
		is_private: bool = True,
		doctype: str | None = None,
		docname: str | None = None,
	) -> str:
		"""Attach a file to a document (defaults to the background task) and return its file URL"""
		if not (doctype and docname):
			if self.ref_doctype and self.ref_docname:
				doctype, docname = self.ref_doctype, self.ref_docname

		file_doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": file_name,
				"attached_to_doctype": doctype or "Background Task",
				"attached_to_name": docname or self.name,
				"content": content,
				"is_private": int(is_private),
			}
		)
		file_doc.insert(ignore_permissions=True)
		return file_doc.file_url

	def _publish(self, message: dict) -> None:
		frappe.publish_realtime(event="task_update", message=message, user=self.user)


@frappe.whitelist()
def stop_task(task_id: str):
	task_name = frappe.db.get_value("Background Task", {"task_id": task_id}, "name")
	if not task_name:
		raise frappe.DoesNotExistError(frappe._("Background Task {0} not found").format(task_id))

	task = frappe.get_doc("Background Task", task_name)

	is_owner = task.user == frappe.session.user
	is_system_manager = "System Manager" in frappe.get_roles(frappe.session.user)
	if not (is_owner or is_system_manager):
		raise frappe.PermissionError(frappe._("Not permitted"))

	if task.status not in ("Queued", "Running"):
		raise frappe.InvalidStatusError(frappe._("Task is not queued or running"))

	from rq.command import send_stop_job_command
	from rq.job import Job

	from frappe.utils.background_jobs import create_job_id, get_redis_conn

	conn = get_redis_conn()
	rq_job_id = create_job_id(task.job_id or task.task_id)
	job = Job.fetch(rq_job_id, connection=conn)

	if task.status == "Queued":
		job.cancel()
	elif task.status == "Running":
		send_stop_job_command(connection=conn, job_id=rq_job_id)

	task.db_set("status", "Cancelled")

	frappe.publish_realtime(
		event="task_update",
		message={"task_id": task.task_id, "status": "Cancelled", "task_name": task.task_name},
		user=task.user,
	)
