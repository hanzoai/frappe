# Copyright (c) 2026, Frappe Technologies and Contributors
# See license.txt

import time

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils.task_queue import enqueue_task, get_current_task


def sample_task(seconds=1):
	handle = get_current_task()
	if handle:
		handle.publish_progress(50, "Halfway there")

	if seconds:
		time.sleep(seconds)

	return "Done!"


class TestBackgroundTask(IntegrationTestCase):
	def test_task_lifecycle(self):
		# 1. Enqueue
		task_id = enqueue_task(sample_task, task_name="Test lifecycle task", seconds=1)

		# 2. Verify record exists and is Queued
		status = frappe.db.get_value("Background Task", {"task_id": task_id}, "status")
		self.assertEqual(status, "Queued")

		# 3. Manually run the worker wrapper (simulating the worker picking it up)
		from frappe.utils.task_queue import _execute_task

		# Note: We pass seconds=0 to make the test run fast
		_execute_task(task_id, sample_task, frappe.session.user, seconds=0)

		# 4. Verify completion
		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Completed")
		self.assertEqual(doc.progress, 100)
		self.assertIn("Done!", doc.result)

	def test_task_failure(self):
		def failing_task():
			raise ValueError("Boom!")

		task_id = enqueue_task(failing_task, task_name="Test failing task")

		from frappe.utils.task_queue import _execute_task

		try:
			_execute_task(task_id, failing_task, frappe.session.user)
		except ValueError:
			pass  # Expected

		doc = frappe.get_doc("Background Task", {"task_id": task_id})
		self.assertEqual(doc.status, "Failed")
		self.assertIn("ValueError: Boom!", doc.exception)
