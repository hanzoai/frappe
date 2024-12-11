import json
from typing import TYPE_CHECKING, Union

import redis

import frappe
from frappe.utils import cstr

if TYPE_CHECKING:
	from frappe.model.document import Document

queue_prefix = "insert_queue_for_"


def deferred_insert(doctype: str, records: list[Union[dict, "Document"]] | str):
	if isinstance(records, dict | list):
		_records = json.dumps(records)
	else:
		_records = records

	try:
<<<<<<< HEAD
		frappe.cache.rpush(f"{queue_prefix}{doctype}", _records)
=======
		frappe.cache().rpush(f"{queue_prefix}{doctype}", _records)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	except redis.exceptions.ConnectionError:
		for record in records:
			insert_record(record, doctype)


def save_to_db():
<<<<<<< HEAD
	queue_keys = frappe.cache.get_keys(queue_prefix)
=======
	queue_keys = frappe.cache().get_keys(queue_prefix)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	for key in queue_keys:
		record_count = 0
		queue_key = get_key_name(key)
		doctype = get_doctype_name(key)
<<<<<<< HEAD
		while frappe.cache.llen(queue_key) > 0 and record_count <= 500:
			records = frappe.cache.lpop(queue_key)
=======
		while frappe.cache().llen(queue_key) > 0 and record_count <= 500:
			records = frappe.cache().lpop(queue_key)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			records = json.loads(records.decode("utf-8"))
			if isinstance(records, dict):
				record_count += 1
				insert_record(records, doctype)
				continue
			for record in records:
				record_count += 1
				insert_record(record, doctype)


def insert_record(record: Union[dict, "Document"], doctype: str):
	try:
		record.update({"doctype": doctype})
		frappe.get_doc(record).insert()
	except Exception as e:
		frappe.logger().error(f"Error while inserting deferred {doctype} record: {e}")


def get_key_name(key: str) -> str:
	return cstr(key).split("|")[1]


def get_doctype_name(key: str) -> str:
	return cstr(key).split(queue_prefix)[1]
