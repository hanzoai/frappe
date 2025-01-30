import os
from pathlib import Path

import click

import frappe
from frappe.database.db_manager import DbManager


def get_sqlite_version() -> str:
	return frappe.db.sql("select sqlite_version()")[0][0]


def setup_database(force, verbose):
	frappe.local.session = frappe._dict({"user": "Administrator"})

	root_conn = get_root_connection()
	root_conn.close()


def bootstrap_database(verbose, source_sql=None):
	import sys

	frappe.connect()

	import_db_from_sql(source_sql, verbose)

	frappe.connect()
	if "tabDefaultValue" not in frappe.db.get_tables(cached=False):
		from click import secho

		secho(
			"Table 'tabDefaultValue' missing in the restored site. "
			"This happens when the backup fails to restore. Please check that the file is valid\n"
			"Do go through the above output to check the exact error message from MariaDB",
			fg="red",
		)
		sys.exit(1)


def import_db_from_sql(source_sql=None, verbose=False):
	if verbose:
		print("Starting database import...")
	db_name = frappe.conf.db_name
	if not source_sql:
		source_sql = os.path.join(os.path.dirname(__file__), "framework_sqlite.sql")
	DbManager(frappe.local.db).restore_database(
		verbose, db_name, source_sql, frappe.conf.db_user, frappe.conf.db_password
	)
	if verbose:
		print("Imported from database {}".format(source_sql))


def drop_database(db_name: str):
	Path(db_name).unlink(missing_ok=True)


def get_root_connection():
	frappe.local.flags.root_connection = frappe.database.get_db(
		cur_db_name=frappe.conf.db_name,
	)

	return frappe.local.flags.root_connection
