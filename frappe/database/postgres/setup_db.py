import os

import frappe
<<<<<<< HEAD
from frappe.database.db_manager import DbManager
from frappe.utils import cint


def setup_database():
	root_conn = get_root_connection(frappe.flags.root_login, frappe.flags.root_password)
	root_conn.commit()
	root_conn.sql("end")
	root_conn.sql(f'DROP DATABASE IF EXISTS "{frappe.conf.db_name}"')

	# If user exists, just update password
	if root_conn.sql(f"SELECT 1 FROM pg_roles WHERE rolname='{frappe.conf.db_name}'"):
		root_conn.sql(f"ALTER USER \"{frappe.conf.db_name}\" WITH PASSWORD '{frappe.conf.db_password}'")
	else:
		root_conn.sql(f"CREATE USER \"{frappe.conf.db_name}\" WITH PASSWORD '{frappe.conf.db_password}'")
	root_conn.sql(f'CREATE DATABASE "{frappe.conf.db_name}"')
	root_conn.sql(f'GRANT ALL PRIVILEGES ON DATABASE "{frappe.conf.db_name}" TO "{frappe.conf.db_name}"')
	if psql_version := root_conn.sql("SHOW server_version_num", as_dict=True):
		semver_version_num = psql_version[0].get("server_version_num") or "140000"
		if cint(semver_version_num) > 150000:
			root_conn.sql(f'ALTER DATABASE "{frappe.conf.db_name}" OWNER TO "{frappe.conf.db_name}"')
	root_conn.close()


def bootstrap_database(verbose, source_sql=None):
	frappe.connect()
	import_db_from_sql(source_sql, verbose)
	frappe.connect()
=======


def setup_database(force, source_sql=None, verbose=False):
	root_conn = get_root_connection(frappe.flags.root_login, frappe.flags.root_password)
	root_conn.commit()
	root_conn.sql("end")
	root_conn.sql(f"DROP DATABASE IF EXISTS `{frappe.conf.db_name}`")
	root_conn.sql(f"DROP USER IF EXISTS {frappe.conf.db_name}")
	root_conn.sql(f"CREATE DATABASE `{frappe.conf.db_name}`")
	root_conn.sql(f"CREATE user {frappe.conf.db_name} password '{frappe.conf.db_password}'")
	root_conn.sql(f"GRANT ALL PRIVILEGES ON DATABASE `{frappe.conf.db_name}` TO {frappe.conf.db_name}")
	root_conn.close()

	bootstrap_database(frappe.conf.db_name, verbose, source_sql=source_sql)
	frappe.connect()


def bootstrap_database(db_name, verbose, source_sql=None):
	frappe.connect(db_name=db_name)
	import_db_from_sql(source_sql, verbose)
	frappe.connect(db_name=db_name)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	if "tabDefaultValue" not in frappe.db.get_tables():
		import sys

		from click import secho

		secho(
			"Table 'tabDefaultValue' missing in the restored site. "
			"This happens when the backup fails to restore. Please check that the file is valid\n"
			"Do go through the above output to check the exact error message from MariaDB",
			fg="red",
		)
		sys.exit(1)


def import_db_from_sql(source_sql=None, verbose=False):
<<<<<<< HEAD
	if verbose:
		print("Starting database import...")
	db_name = frappe.conf.db_name
	if not source_sql:
		source_sql = os.path.join(os.path.dirname(__file__), "framework_postgres.sql")
	DbManager(frappe.local.db).restore_database(
		verbose, db_name, source_sql, db_name, frappe.conf.db_password
	)
	if verbose:
		print("Imported from database %s" % source_sql)
=======
	from shutil import which
	from subprocess import PIPE, run

	# we can't pass psql password in arguments in postgresql as mysql. So
	# set password connection parameter in environment variable
	subprocess_env = os.environ.copy()
	subprocess_env["PGPASSWORD"] = str(frappe.conf.db_password)

	# bootstrap db
	if not source_sql:
		source_sql = os.path.join(os.path.dirname(__file__), "framework_postgres.sql")

	pv = which("pv")

	_command = (
		f"psql {frappe.conf.db_name} "
		f"-h {frappe.conf.db_host or 'localhost'} -p {frappe.conf.db_port or '5432'!s} "
		f"-U {frappe.conf.db_name}"
	)

	if pv:
		command = f"{pv} {source_sql} | " + _command
	else:
		command = _command + f" -f {source_sql}"

	print("Restoring Database file...")
	if verbose:
		print(command)

	restore_proc = run(command, env=subprocess_env, shell=True, stdout=PIPE)

	if verbose:
		print(f"\nSTDOUT by psql:\n{restore_proc.stdout.decode()}\nImported from Database File: {source_sql}")


def setup_help_database(help_db_name):
	root_conn = get_root_connection(frappe.flags.root_login, frappe.flags.root_password)
	root_conn.sql(f"DROP DATABASE IF EXISTS `{help_db_name}`")
	root_conn.sql(f"DROP USER IF EXISTS {help_db_name}")
	root_conn.sql(f"CREATE DATABASE `{help_db_name}`")
	root_conn.sql(f"CREATE user {help_db_name} password '{help_db_name}'")
	root_conn.sql(f"GRANT ALL PRIVILEGES ON DATABASE `{help_db_name}` TO {help_db_name}")
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)


def get_root_connection(root_login=None, root_password=None):
	if not frappe.local.flags.root_connection:
		if not root_login:
			root_login = frappe.conf.get("root_login") or None

		if not root_login:
			root_login = input("Enter postgres super user: ")

		if not root_password:
			root_password = frappe.conf.get("root_password") or None

		if not root_password:
			from getpass import getpass

			root_password = getpass("Postgres super user password: ")

<<<<<<< HEAD
		frappe.local.flags.root_connection = frappe.database.get_db(
			socket=frappe.conf.db_socket,
			host=frappe.conf.db_host,
			port=frappe.conf.db_port,
			user=root_login,
			password=root_password,
			cur_db_name=root_login,
		)
=======
		frappe.local.flags.root_connection = frappe.database.get_db(user=root_login, password=root_password)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)

	return frappe.local.flags.root_connection


def drop_user_and_database(db_name, root_login, root_password):
	root_conn = get_root_connection(
		frappe.flags.root_login or root_login, frappe.flags.root_password or root_password
	)
	root_conn.commit()
	root_conn.sql(
		"SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = %s",
		(db_name,),
	)
	root_conn.sql("end")
	root_conn.sql(f"DROP DATABASE IF EXISTS {db_name}")
	root_conn.sql(f"DROP USER IF EXISTS {db_name}")
