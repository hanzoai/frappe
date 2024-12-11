# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# Database Module
# --------------------
<<<<<<< HEAD
from shutil import which
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

from frappe.database.database import savepoint


<<<<<<< HEAD
def setup_database(force, verbose=None, mariadb_user_host_login_scope=None):
=======
def setup_database(force, source_sql=None, verbose=None, no_mariadb_socket=False):
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	import frappe

	if frappe.conf.db_type == "postgres":
		import frappe.database.postgres.setup_db

<<<<<<< HEAD
		return frappe.database.postgres.setup_db.setup_database()
	else:
		import frappe.database.mariadb.setup_db

		return frappe.database.mariadb.setup_db.setup_database(force, verbose, mariadb_user_host_login_scope)


def bootstrap_database(verbose=None, source_sql=None):
	import frappe

	if frappe.conf.db_type == "postgres":
		import frappe.database.postgres.setup_db

		return frappe.database.postgres.setup_db.bootstrap_database(verbose, source_sql)
	else:
		import frappe.database.mariadb.setup_db

		return frappe.database.mariadb.setup_db.bootstrap_database(verbose, source_sql)
=======
		return frappe.database.postgres.setup_db.setup_database(force, source_sql, verbose)
	else:
		import frappe.database.mariadb.setup_db

		return frappe.database.mariadb.setup_db.setup_database(
			force, source_sql, verbose, no_mariadb_socket=no_mariadb_socket
		)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def drop_user_and_database(db_name, root_login=None, root_password=None):
	import frappe

	if frappe.conf.db_type == "postgres":
		import frappe.database.postgres.setup_db

		return frappe.database.postgres.setup_db.drop_user_and_database(db_name, root_login, root_password)
	else:
		import frappe.database.mariadb.setup_db

		return frappe.database.mariadb.setup_db.drop_user_and_database(db_name, root_login, root_password)


<<<<<<< HEAD
def get_db(host=None, user=None, password=None, port=None, cur_db_name=None, socket=None):
=======
def get_db(host=None, user=None, password=None, port=None):
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	import frappe

	if frappe.conf.db_type == "postgres":
		import frappe.database.postgres.database

<<<<<<< HEAD
		return frappe.database.postgres.database.PostgresDatabase(
			host, user, password, port, cur_db_name, socket
		)
	else:
		import frappe.database.mariadb.database

		return frappe.database.mariadb.database.MariaDBDatabase(
			host, user, password, port, cur_db_name, socket
		)


def get_command(
	host=None, port=None, user=None, password=None, db_name=None, extra=None, dump=False, socket=None
):
	import frappe

	if frappe.conf.db_type == "postgres":
		if dump:
			bin, bin_name = which("pg_dump"), "pg_dump"
		else:
			bin, bin_name = which("psql"), "psql"

		if socket and password:
			conn_string = f"postgresql://{user}:{password}@/{db_name}?host={socket}"
		elif socket:
			conn_string = f"postgresql://{user}@/{db_name}?host={socket}"
		elif password:
			conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
		else:
			conn_string = f"postgresql://{user}@{host}:{port}/{db_name}"

		command = [conn_string]

		if extra:
			command.extend(extra)

	else:
		if dump:
			bin, bin_name = which("mariadb-dump") or which("mysqldump"), "mariadb-dump"
		else:
			bin, bin_name = which("mariadb") or which("mysql"), "mariadb"

		command = [f"--user={user}"]
		if socket:
			command.append(f"--socket={socket}")
		elif host and port:
			command.append(f"--host={host}")
			command.append(f"--port={port}")

		if password:
			command.append(f"--password={password}")

		if dump:
			command.extend(
				[
					"--single-transaction",
					"--quick",
					"--lock-tables=false",
				]
			)
		else:
			command.extend(
				[
					"--pager=less -SFX",
					"--safe-updates",
					"--no-auto-rehash",
				]
			)

		command.append(db_name)

		if extra:
			command.extend(extra)

	return bin, command, bin_name
=======
		return frappe.database.postgres.database.PostgresDatabase(host, user, password, port=port)
	else:
		import frappe.database.mariadb.database

		return frappe.database.mariadb.database.MariaDBDatabase(host, user, password, port=port)


def setup_help_database(help_db_name):
	import frappe

	if frappe.conf.db_type == "postgres":
		import frappe.database.postgres.setup_db

		return frappe.database.postgres.setup_db.setup_help_database(help_db_name)
	else:
		import frappe.database.mariadb.setup_db

		return frappe.database.mariadb.setup_db.setup_help_database(help_db_name)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
