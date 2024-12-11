# Copyright (c) 2021, Frappe Technologies and Contributors
# License: MIT. See LICENSE

import frappe
from frappe.test_runner import make_test_records
from frappe.tests.utils import FrappeTestCase
<<<<<<< HEAD

TEST_DOCTYPE = "Assignment Test"
=======
from frappe.utils import random_string
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


class TestAutoAssign(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.db.delete("Assignment Rule")
<<<<<<< HEAD
		create_test_doctype(TEST_DOCTYPE)
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()

	def setUp(self):
<<<<<<< HEAD
		frappe.set_user("Administrator")
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		make_test_records("User")
		days = [
			dict(day="Sunday"),
			dict(day="Monday"),
			dict(day="Tuesday"),
			dict(day="Wednesday"),
			dict(day="Thursday"),
			dict(day="Friday"),
			dict(day="Saturday"),
		]
		self.days = days
		self.assignment_rule = get_assignment_rule([days, days])
		clear_assignments()

	def test_round_robin(self):
<<<<<<< HEAD
		# check if auto assigned to first user
		record = _make_test_record(public=1)
		self.assertEqual(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		# check if auto assigned to first user
		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			"test@example.com",
		)

<<<<<<< HEAD
		# check if auto assigned to second user
		record = _make_test_record(public=1)
		self.assertEqual(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		# check if auto assigned to second user
		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			"test1@example.com",
		)

		clear_assignments()

<<<<<<< HEAD
		# check if auto assigned to third user, even if
		# previous assignments where closed
		record = _make_test_record(public=1)
		self.assertEqual(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		# check if auto assigned to third user, even if
		# previous assignments where closed
		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			"test2@example.com",
		)

		# check loop back to first user
<<<<<<< HEAD
		record = _make_test_record(public=1)
		self.assertEqual(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			"test@example.com",
		)

	def test_load_balancing(self):
		self.assignment_rule.rule = "Load Balancing"
		self.assignment_rule.save()

		for _ in range(30):
<<<<<<< HEAD
			_make_test_record(public=1)

		# check if each user has 10 assignments (?)
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(
				len(frappe.get_all("ToDo", dict(allocated_to=user, reference_type=TEST_DOCTYPE))), 10
			)
=======
			make_note(dict(public=1))

		# check if each user has 10 assignments (?)
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(len(frappe.get_all("ToDo", dict(allocated_to=user, reference_type="Note"))), 10)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

		# clear 5 assignments for first user
		# can't do a limit in "delete" since postgres does not support it
		for d in frappe.get_all(
<<<<<<< HEAD
			"ToDo", dict(reference_type=TEST_DOCTYPE, allocated_to="test@example.com"), limit=5
=======
			"ToDo", dict(reference_type="Note", allocated_to="test@example.com"), limit=5
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		):
			frappe.db.delete("ToDo", {"name": d.name})

		# add 5 more assignments
<<<<<<< HEAD
		for _ in range(5):
			_make_test_record(public=1)

		# check if each user still has 10 assignments
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(
				len(frappe.get_all("ToDo", dict(allocated_to=user, reference_type=TEST_DOCTYPE))), 10
			)
=======
		for _i in range(5):
			make_note(dict(public=1))

		# check if each user still has 10 assignments
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(len(frappe.get_all("ToDo", dict(allocated_to=user, reference_type="Note"))), 10)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	def test_assingment_on_guest_submissions(self):
		"""Sometimes documents are inserted as guest, check if assignment rules run on them. Use case: Web Forms"""
		with self.set_user("Guest"):
<<<<<<< HEAD
			doc = _make_test_record(ignore_permissions=True, public=1)
=======
			doc = make_note({"public": 1}, ignore_permissions=True)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

		# check assignment to *anyone*
		self.assertTrue(
			frappe.db.get_value(
				"ToDo",
<<<<<<< HEAD
				{"reference_type": TEST_DOCTYPE, "reference_name": doc.name, "status": "Open"},
=======
				{"reference_type": "Note", "reference_name": doc.name, "status": "Open"},
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
				"allocated_to",
			),
		)

	def test_based_on_field(self):
		self.assignment_rule.rule = "Based on Field"
		self.assignment_rule.field = "owner"
		self.assignment_rule.save()

<<<<<<< HEAD
		for test_user in ("test1@example.com", "test2@example.com"):
			frappe.set_user(test_user)
			note = _make_test_record(public=1)
			# check if auto assigned to doc owner, test1@example.com
			self.assertEqual(
				frappe.db.get_value(
					"ToDo",
					dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
					"owner",
				),
				test_user,
			)

	def test_assign_condition(self):
		# check condition
		note = _make_test_record(public=0)

		self.assertEqual(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
=======
		frappe.set_user("test1@example.com")
		note = make_note(dict(public=1))
		# check if auto assigned to doc owner, test1@example.com
		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "owner"
			),
			"test1@example.com",
		)

		frappe.set_user("test2@example.com")
		note = make_note(dict(public=1))
		# check if auto assigned to doc owner, test2@example.com
		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "owner"
			),
			"test2@example.com",
		)

		frappe.set_user("Administrator")

	def test_assign_condition(self):
		# check condition
		note = make_note(dict(public=0))

		self.assertEqual(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			None,
		)

	def test_clear_assignment(self):
<<<<<<< HEAD
		note = _make_test_record(public=1)

		# check if auto assigned to first user
		todo = frappe.get_list(
			"ToDo", dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"), limit=1
=======
		note = make_note(dict(public=1))

		# check if auto assigned to first user
		todo = frappe.get_list(
			"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), limit=1
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		)[0]

		todo = frappe.get_doc("ToDo", todo["name"])
		self.assertEqual(todo.allocated_to, "test@example.com")

		# test auto unassign
		note.public = 0
		note.save()

		todo.load_from_db()

		# check if todo is cancelled
		self.assertEqual(todo.status, "Cancelled")

	def test_close_assignment(self):
<<<<<<< HEAD
		note = _make_test_record(public=1, content="valid")

		# check if auto assigned
		todo = frappe.get_list(
			"ToDo", dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"), limit=1
=======
		note = make_note(dict(public=1, content="valid"))

		# check if auto assigned
		todo = frappe.get_list(
			"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), limit=1
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		)[0]

		todo = frappe.get_doc("ToDo", todo["name"])
		self.assertEqual(todo.allocated_to, "test@example.com")

		note.content = "Closed"
		note.save()

		todo.load_from_db()

		# check if todo is closed
		self.assertEqual(todo.status, "Closed")
		# check if closed todo retained assignment
		self.assertEqual(todo.allocated_to, "test@example.com")

	def check_multiple_rules(self):
<<<<<<< HEAD
		note = _make_test_record(public=1, notify_on_login=1)
=======
		note = make_note(dict(public=1, notify_on_login=1))
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

		# check if auto assigned to test3 (2nd rule is applied, as it has higher priority)
		self.assertEqual(
			frappe.db.get_value(
<<<<<<< HEAD
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
=======
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			"test@example.com",
		)

	def check_assignment_rule_scheduling(self):
		frappe.db.delete("Assignment Rule")

		days_1 = [dict(day="Sunday"), dict(day="Monday"), dict(day="Tuesday")]

		days_2 = [dict(day="Wednesday"), dict(day="Thursday"), dict(day="Friday"), dict(day="Saturday")]

		get_assignment_rule([days_1, days_2], ["public == 1", "public == 1"])

		frappe.flags.assignment_day = "Monday"
<<<<<<< HEAD
		note = _make_test_record(public=1)

		self.assertIn(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		self.assertIn(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			["test@example.com", "test1@example.com", "test2@example.com"],
		)

		frappe.flags.assignment_day = "Friday"
<<<<<<< HEAD
		note = _make_test_record(public=1)

		self.assertIn(
			frappe.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
=======
		note = make_note(dict(public=1))

		self.assertIn(
			frappe.db.get_value(
				"ToDo", dict(reference_type="Note", reference_name=note.name, status="Open"), "allocated_to"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			),
			["test3@example.com"],
		)

	def test_assignment_rule_condition(self):
		frappe.db.delete("Assignment Rule")

<<<<<<< HEAD
=======
		# Add expiry_date custom field
		from frappe.custom.doctype.custom_field.custom_field import create_custom_field

		df = dict(fieldname="expiry_date", label="Expiry Date", fieldtype="Date")
		create_custom_field("Note", df)

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		assignment_rule = frappe.get_doc(
			dict(
				name="Assignment with Due Date",
				doctype="Assignment Rule",
<<<<<<< HEAD
				document_type=TEST_DOCTYPE,
=======
				document_type="Note",
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
				assign_condition="public == 0",
				due_date_based_on="expiry_date",
				assignment_days=self.days,
				users=[
					dict(user="test@example.com"),
				],
			)
		).insert()

		expiry_date = frappe.utils.add_days(frappe.utils.nowdate(), 2)
<<<<<<< HEAD
		note1 = _make_test_record(expiry_date=expiry_date)
		note2 = _make_test_record(expiry_date=expiry_date)

		note1_todo = frappe.get_all(
			"ToDo", filters=dict(reference_type=TEST_DOCTYPE, reference_name=note1.name, status="Open")
=======
		note1 = make_note({"expiry_date": expiry_date})
		note2 = make_note({"expiry_date": expiry_date})

		note1_todo = frappe.get_all(
			"ToDo", filters=dict(reference_type="Note", reference_name=note1.name, status="Open")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		)[0]

		note1_todo_doc = frappe.get_doc("ToDo", note1_todo.name)
		self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), expiry_date)

		# due date should be updated if the reference doc's date is updated.
		note1.expiry_date = frappe.utils.add_days(expiry_date, 2)
		note1.save()
		note1_todo_doc.reload()
		self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), note1.expiry_date)

		# saving one note's expiry should not update other note todo's due date
		note2_todo = frappe.get_all(
			"ToDo",
<<<<<<< HEAD
			filters=dict(reference_type=TEST_DOCTYPE, reference_name=note2.name, status="Open"),
=======
			filters=dict(reference_type="Note", reference_name=note2.name, status="Open"),
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			fields=["name", "date"],
		)[0]
		self.assertNotEqual(frappe.utils.get_date_str(note2_todo.date), note1.expiry_date)
		self.assertEqual(frappe.utils.get_date_str(note2_todo.date), expiry_date)
		assignment_rule.delete()
		frappe.db.commit()  # undo changes commited by DDL

	def test_submittable_assignment(self):
		# create a submittable doctype
		submittable_doctype = "Assignment Test Submittable"
		create_test_doctype(submittable_doctype)
		dt = frappe.get_doc("DocType", submittable_doctype)
		dt.is_submittable = 1
		dt.save()

		# create a rule for the submittable doctype
		assignment_rule = frappe.new_doc("Assignment Rule")
		assignment_rule.name = f"For {submittable_doctype}"
		assignment_rule.document_type = submittable_doctype
		assignment_rule.rule = "Round Robin"
		assignment_rule.extend("assignment_days", self.days)
		assignment_rule.append("users", {"user": "test@example.com"})
		assignment_rule.assign_condition = "docstatus == 1"
		assignment_rule.unassign_condition = "docstatus == 2"
		assignment_rule.save()

		# create a submittable doc
		doc = frappe.new_doc(submittable_doctype)
		doc.save()
		doc.submit()

		# check if todo is created
		todos = frappe.get_all(
			"ToDo",
			filters={
				"reference_type": submittable_doctype,
				"reference_name": doc.name,
				"status": "Open",
				"allocated_to": "test@example.com",
			},
		)
		self.assertEqual(len(todos), 1)

		# check if todo is closed on cancel
		doc.cancel()
		todos = frappe.get_all(
			"ToDo",
			filters={
				"reference_type": submittable_doctype,
				"reference_name": doc.name,
				"status": "Cancelled",
				"allocated_to": "test@example.com",
			},
		)
		self.assertEqual(len(todos), 1)


def clear_assignments():
<<<<<<< HEAD
	frappe.db.delete("ToDo", {"reference_type": TEST_DOCTYPE})


def get_assignment_rule(days, assign=None):
	frappe.delete_doc_if_exists("Assignment Rule", f"For {TEST_DOCTYPE} 1")
=======
	frappe.db.delete("ToDo", {"reference_type": "Note"})


def get_assignment_rule(days, assign=None):
	frappe.delete_doc_if_exists("Assignment Rule", "For Note 1")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	if not assign:
		assign = ["public == 1", "notify_on_login == 1"]

	assignment_rule = frappe.get_doc(
		dict(
<<<<<<< HEAD
			name=f"For {TEST_DOCTYPE} 1",
			doctype="Assignment Rule",
			priority=0,
			document_type=TEST_DOCTYPE,
=======
			name="For Note 1",
			doctype="Assignment Rule",
			priority=0,
			document_type="Note",
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			assign_condition=assign[0],
			unassign_condition="public == 0 or notify_on_login == 1",
			close_condition='"Closed" in content',
			rule="Round Robin",
			assignment_days=days[0],
			users=[
				dict(user="test@example.com"),
				dict(user="test1@example.com"),
				dict(user="test2@example.com"),
			],
		)
	).insert()

<<<<<<< HEAD
	frappe.delete_doc_if_exists("Assignment Rule", f"For {TEST_DOCTYPE} 2")
=======
	frappe.delete_doc_if_exists("Assignment Rule", "For Note 2")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	# 2nd rule
	frappe.get_doc(
		dict(
<<<<<<< HEAD
			name=f"For {TEST_DOCTYPE} 2",
			doctype="Assignment Rule",
			priority=1,
			document_type=TEST_DOCTYPE,
=======
			name="For Note 2",
			doctype="Assignment Rule",
			priority=1,
			document_type="Note",
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			assign_condition=assign[1],
			unassign_condition="notify_on_login == 0",
			rule="Round Robin",
			assignment_days=days[1],
			users=[dict(user="test3@example.com")],
		)
	).insert()

	return assignment_rule


<<<<<<< HEAD
def _make_test_record(
	*,
	ignore_permissions=False,
	**kwargs,
):
	doc = frappe.new_doc(TEST_DOCTYPE)

	if kwargs:
		doc.update(kwargs)

	return doc.insert(ignore_permissions=ignore_permissions)
=======
def make_note(values=None, *, ignore_permissions=False):
	note = frappe.get_doc(dict(doctype="Note", title=random_string(10), content=random_string(20)))

	if values:
		note.update(values)

	note.insert(ignore_permissions=ignore_permissions)

	return note
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def create_test_doctype(doctype: str):
	"""Create custom doctype."""
	frappe.delete_doc("DocType", doctype)

	frappe.get_doc(
		{
			"doctype": "DocType",
			"name": doctype,
			"module": "Custom",
			"custom": 1,
			"fields": [
				{
					"fieldname": "expiry_date",
					"label": "Expiry Date",
					"fieldtype": "Date",
				},
				{
					"fieldname": "notify_on_login",
					"label": "Notify on Login",
					"fieldtype": "Check",
				},
				{
					"fieldname": "public",
					"label": "Public",
					"fieldtype": "Check",
				},
				{
					"fieldname": "content",
					"label": "Content",
					"fieldtype": "Text",
				},
			],
			"permissions": [
				{
					"create": 1,
					"delete": 1,
					"email": 1,
					"export": 1,
					"print": 1,
					"read": 1,
					"report": 1,
					"role": "All",
					"share": 1,
					"write": 1,
				},
			],
		}
	).insert()
