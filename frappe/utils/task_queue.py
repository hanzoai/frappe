import time
from collections.abc import Callable
from uuid import uuid4

import frappe
from frappe import _

PUBLISH_THROTTLE_SECONDS = 0.2


def enqueue_task(
	method: str | Callable,
	*,
	task_name: str | None = None,
	queue: str = "default",
	timeout: int | None = None,
	event: str | None = None,
	ref_doctype: str | None = None,
	ref_docname: str | None = None,
	deduplicate: bool = False,
	job_id: str | None = None,
	enqueue_after_commit: bool = False,
	now: bool = False,
	on_success: Callable | None = None,
	on_failure: Callable | None = None,
	show_progress_bar: bool = True,
	at_front: bool = False,
	at_front_when_starved: bool = False,
	**kwargs,
) -> str:
	"""A wrapper around frappe.enqueue. Enqueue a background job with user-facing tracking"""
	if isinstance(method, Callable):
		method_name = f"{method.__module__}.{method.__qualname__}"
	else:
		method_name = method

	if not task_name:
		task_name = method_name

	task_id = str(uuid4())
	user = frappe.session.user

	try:
		arguments_json = frappe.as_json(kwargs) if kwargs else None
	except Exception:
		arguments_json = None

	def _create_and_enqueue():
		doc = frappe.new_doc("Background Task")
		doc.task_id = task_id
		doc.job_id = job_id or task_id
		doc.task_name = task_name
		doc.status = "Queued"
		doc.user = user
		doc.method = method_name
		doc.arguments = arguments_json
		doc.queue = queue
		doc.show_progress_bar = show_progress_bar
		if ref_doctype:
			doc.ref_doctype = ref_doctype
		if ref_docname:
			doc.ref_docname = ref_docname
		doc.insert(ignore_permissions=True)

		frappe.publish_realtime(
			event="task_update",
			message={"task_id": task_id, "task_name": task_name, "status": "Queued"},
			user=user,
		)

		if frappe.db.get_value("Background Task", {"task_id": task_id}, "status") == "Cancelled":
			return

		frappe.enqueue(
			_execute_task,
			queue=queue,
			timeout=timeout,
			event=event,
			deduplicate=deduplicate,
			job_id=job_id or task_id,
			on_success=on_success,
			on_failure=on_failure,
			at_front=at_front,
			now=now,
			at_front_when_starved=at_front_when_starved,
			task_id=task_id,
			target_method=method,
			task_user=user,
			**kwargs,
		)

	if enqueue_after_commit:
		frappe.db.after_commit.add(_create_and_enqueue)
	else:
		_create_and_enqueue()

	return task_id


def get_current_task() -> "TaskHandle | None":
	return getattr(frappe.local, "_current_task_handle", None)


def get_task_status(task_id: str) -> dict | None:
	fields = ["status", "progress", "stage", "result", "exception", "started_at", "ended_at"]
	return frappe.db.get_value("Background Task", {"task_id": task_id}, fields, as_dict=True)


class TaskHandle:
	"""Handle for publishing updates from within a running background task"""

	def __init__(self, task_id: str, user: str, task_name: str):
		self.task_id = task_id
		self.user = user
		self.task_name = task_name
		self._last_published: float = 0.0

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
		frappe.db.set_value(
			"Background Task",
			{"task_id": self.task_id},
			"result",
			frappe.as_json(result),
			update_modified=False,
		)

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
			ref_doctype, ref_docname = frappe.db.get_value(
				"Background Task", {"task_id": self.task_id}, ["ref_doctype", "ref_docname"]
			)
			if ref_doctype and ref_docname:
				doctype, docname = ref_doctype, ref_docname

		file_doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": file_name,
				"attached_to_doctype": doctype or "Background Task",
				"attached_to_name": docname or self.task_id,
				"content": content,
				"is_private": int(is_private),
			}
		)
		file_doc.insert(ignore_permissions=True)
		return file_doc.file_url

	def _publish(self, message: dict) -> None:
		frappe.publish_realtime(event="task_update", message=message, user=self.user)


def _execute_task(task_id: str, target_method: str | Callable, task_user: str, **kwargs):
	"""Internal wrapper run by the background worker"""
	task_doc_filters = {"task_id": task_id}
	task_name = frappe.db.get_value("Background Task", task_doc_filters, "task_name") or "Background Task"
	if frappe.db.get_value("Background Task", task_doc_filters, "status") == "Cancelled":
		return

	handle = TaskHandle(task_id, task_user, task_name)
	frappe.local._current_task_handle = handle

	frappe.db.set_value(
		"Background Task",
		task_doc_filters,
		{"status": "Running", "started_at": frappe.utils.now()},
		update_modified=False,
	)
	frappe.db.commit()

	handle._publish({"task_id": task_id, "task_name": task_name, "status": "Running"})

	try:
		if isinstance(target_method, str):
			target_method = frappe.get_attr(target_method)

		result = target_method(**kwargs)

		values = {"status": "Completed", "progress": 100, "ended_at": frappe.utils.now()}
		if result is not None:
			try:
				values["result"] = frappe.as_json(result)
			except Exception:
				pass

		frappe.db.set_value("Background Task", task_doc_filters, values, update_modified=False)
		frappe.db.commit()
		handle._publish({"task_id": task_id, "task_name": task_name, "status": "Completed", "progress": 100})

		return result

	except Exception:
		frappe.db.rollback()
		frappe.db.set_value(
			"Background Task",
			task_doc_filters,
			{
				"status": "Failed",
				"exception": frappe.get_traceback(with_context=True),
				"ended_at": frappe.utils.now(),
			},
			update_modified=False,
		)
		frappe.db.commit()

		handle._publish({"task_id": task_id, "task_name": task_name, "status": "Failed"})

		raise

	finally:
		frappe.local._current_task_handle = None
