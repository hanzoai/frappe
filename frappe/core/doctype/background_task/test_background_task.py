import time
from unittest.mock import patch

import frappe
from frappe.core.doctype.doctype.test_doctype import new_doctype
from frappe.tests import IntegrationTestCase
from frappe.utils.task_queue import _execute_task, enqueue_task, get_current_task, get_task_status


def sample_task(value=1):
	return {"value": value}


def sample_task_with_updates(total=3):
	handle = get_current_task()
	for i in range(1, total + 1):
		handle.update_stage(f"Step {i}")
		handle.publish_progress((i / total) * 100)
		if i < total:
			time.sleep(0.3)


def sample_task_intermediate_result():
	handle = get_current_task()
	handle.store_result({"partial": True})


def sample_task_with_attachment():
	handle = get_current_task()
	handle.attach_file(file_name="bg-task-output.txt", content=b"done")
	return {"success": True}


def failing_task():
	raise ValueError("Intentional test failure")


class IntegrationTestBackgroundTask(IntegrationTestCase):
	def test_enqueue_and_success_lifecycle(self):
		task_id = enqueue_task(sample_task, task_name="Test success", value=42)
		self.assertEqual(get_task_status(task_id)["status"], "Queued")

		_execute_task(task_id, sample_task, frappe.session.user, value=42)

		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Completed")
		self.assertIn("42", doc.result)

	def test_failed_task_stores_exception(self):
		task_id = enqueue_task(failing_task)
		with self.assertRaises(ValueError):
			_execute_task(task_id, failing_task, frappe.session.user)

		status, exception = frappe.db.get_value(
			"Background Task", {"task_id": task_id}, ["status", "exception"]
		)
		self.assertEqual(status, "Failed")
		self.assertIn("Intentional test failure", exception)

	@patch("frappe.publish_realtime")
	def test_task_with_realtime_updates(self, publish_mock):
		task_id = enqueue_task(sample_task_with_updates, task_name="Updates", total=2)

		# Clear mock so it doesn't count the 'Queued' publish from enqueue_task
		publish_mock.reset_mock()

		_execute_task(task_id, sample_task_with_updates, frappe.session.user, total=2)

		updates = [
			call.kwargs["message"]
			for call in publish_mock.call_args_list
			if call.kwargs.get("event") == "task_update"
		]

		self.assertEqual(updates[0]["status"], "Running")
		self.assertEqual(updates[1]["stage"], "Step 1")
		self.assertEqual(updates[2]["progress"], 50)
		self.assertEqual(updates[3]["stage"], "Step 2")
		self.assertEqual(updates[4]["progress"], 100)
		self.assertEqual(updates[5]["status"], "Completed")

	def test_enqueue_after_commit(self):
		task_id = enqueue_task(sample_task, enqueue_after_commit=True)
		self.assertIsNone(frappe.db.get_value("Background Task", {"task_id": task_id}, "name"))

		frappe.db.commit()
		self.assertEqual(frappe.db.get_value("Background Task", {"task_id": task_id}, "status"), "Queued")

	def test_store_result_during_execution(self):
		task_id = enqueue_task(sample_task_intermediate_result)
		_execute_task(task_id, sample_task_intermediate_result, frappe.session.user)

		self.assertIn("partial", frappe.db.get_value("Background Task", {"task_id": task_id}, "result"))

	@patch("frappe.utils.task_queue.frappe.enqueue")
	@patch("frappe.utils.task_queue.frappe.publish_realtime")
	def test_cancelled_before_enqueue_is_not_enqueued(self, publish_realtime_mock, enqueue_mock):
		def cancel_task(*args, **kwargs):
			message = kwargs.get("message") or {}
			task_id = message.get("task_id")
			if task_id and message.get("status") == "Queued":
				frappe.db.set_value(
					"Background Task", {"task_id": task_id}, "status", "Cancelled", update_modified=False
				)

		publish_realtime_mock.side_effect = cancel_task

		task_id = enqueue_task(sample_task, enqueue_after_commit=True)
		frappe.db.commit()

		self.assertFalse(enqueue_mock.called)
		self.assertEqual(frappe.db.get_value("Background Task", {"task_id": task_id}, "status"), "Cancelled")

	def test_execute_task_skips_if_cancelled(self):
		task_id = enqueue_task(sample_task)
		frappe.db.set_value("Background Task", {"task_id": task_id}, "status", "Cancelled")

		_execute_task(task_id, sample_task, frappe.session.user)

		self.assertEqual(frappe.db.get_value("Background Task", {"task_id": task_id}, "status"), "Cancelled")

	def test_attach_file_links_file_to_task(self):
		task_id = enqueue_task(sample_task_with_attachment)
		_execute_task(task_id, sample_task_with_attachment, frappe.session.user)

		task_doc = frappe.get_doc("Background Task", {"task_id": task_id})
		attached_files = frappe.get_all(
			"File",
			filters={"attached_to_doctype": "Background Task", "attached_to_name": task_doc.name},
			pluck="name",
		)
		self.assertTrue(len(attached_files) > 0)

	def test_attach_file_prefers_ref_document(self):
		test_doctype = new_doctype().insert()
		test_doc = frappe.get_doc({"doctype": test_doctype.name}).insert()

		task_id = enqueue_task(
			sample_task_with_attachment,
			ref_doctype=test_doctype.name,
			ref_docname=test_doc.name,
		)
		_execute_task(task_id, sample_task_with_attachment, frappe.session.user)

		attached_files = frappe.get_all(
			"File",
			filters={"attached_to_doctype": test_doctype.name, "attached_to_name": test_doc.name},
			pluck="name",
		)
		self.assertTrue(len(attached_files) > 0)

	def test_task_handle_cleared_after_execution(self):
		task_id = enqueue_task(sample_task)
		_execute_task(task_id, sample_task, frappe.session.user)
		self.assertIsNone(get_current_task())

	def test_method_passed_as_string(self):
		method_path = "frappe.core.doctype.background_task.test_background_task.sample_task"
		task_id = enqueue_task(method_path, value=99)
		_execute_task(task_id, method_path, frappe.session.user, value=99)

		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Completed")
		self.assertIn("99", doc.result)
