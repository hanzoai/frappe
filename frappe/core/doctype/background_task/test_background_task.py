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
	def setUp(self):
		super().setUp()
		# prevent enqueue_task from creating real RQ jobs in Redis.
		self.enqueue_patcher = patch("frappe.utils.task_queue.frappe.enqueue")
		self.mock_enqueue = self.enqueue_patcher.start()

	def tearDown(self):
		self.enqueue_patcher.stop()
		super().tearDown()

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

		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Failed")
		self.assertIn("Intentional test failure", doc.exception)

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

	@patch("rq.job.Job.fetch")
	def test_stop_task_cancels_queued_task(self, mock_job_fetch):
		from frappe.core.doctype.background_task.background_task import stop_task

		task_id = enqueue_task(sample_task, enqueue_after_commit=False)

		# Cancel the queued task
		stop_task(task_id)

		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Cancelled")

		# If execute is called (worker picking it up later), it should abort early
		_execute_task(task_id, sample_task, frappe.session.user)

		doc.reload()
		self.assertEqual(doc.status, "Cancelled")
		self.assertIsNone(doc.result)
