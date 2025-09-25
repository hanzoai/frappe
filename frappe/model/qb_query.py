# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
"""Query implementation using frappe's query builder"""

import copy
import json
from typing import Any

import frappe
from frappe.database.utils import DefaultOrderBy, FilterValue
from frappe.deprecation_dumpster import deprecation_warning
from frappe.model.utils import is_virtual_doctype
from frappe.model.utils.user_settings import get_user_settings, update_user_settings
from frappe.query_builder.utils import Column


class DatabaseQuery:
	"""
	Copy of db_query.py DatabaseQuery, using query builder instead.
	"""

	def __init__(self, doctype: str) -> None:
		self.doctype = doctype

	def execute(
		self,
		fields: list[str] | tuple[str, ...] | str | None = None,
		filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None,
		or_filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None,
		group_by: str | None = None,
		order_by: str = DefaultOrderBy,
		limit: int | None = None,
		offset: int | None = None,
		limit_start: int = 0,
		limit_page_length: int | None = None,
		as_list: bool = False,
		with_childnames: bool = False,
		debug: bool = False,
		ignore_permissions: bool = False,
		user: str | None = None,
		with_comment_count: bool = False,
		join: str = "left join",
		distinct: bool = False,
		start: int | None = None,
		page_length: int | None = None,
		ignore_ifnull: bool = False,
		save_user_settings: bool = False,
		save_user_settings_fields: bool = False,
		update: dict[str, Any] | None = None,
		user_settings: str | dict[str, Any] | None = None,
		reference_doctype: str | None = None,
		run: bool = True,
		strict: bool = True,
		pluck: str | None = None,
		ignore_ddl: bool = False,
		*,
		parent_doctype: str | None = None,
	) -> list:
		"""Execute a database query using the Query Builder engine.

		Args:
			fields: Fields to select. Can be a list, tuple, or comma-separated string.
			filters: Main filter conditions. Supports dicts, lists, and operator tuples.
			or_filters: Additional filter conditions to be combined with OR.
			group_by: Fields to group results by.
			order_by: Fields to order results by.
			limit: Maximum number of records to return.
			offset: Number of records to skip for pagination.
			limit_start: Legacy pagination start (deprecated, use offset).
			limit_page_length: Legacy pagination length (deprecated, use limit).
			as_list: Return results as list of lists instead of list of dicts.
			with_childnames: Include child document names (not implemented).
			debug: Enable debug mode for query inspection.
			ignore_permissions: Skip permission checks for the query.
			user: Execute query as specific user.
			with_comment_count: Add comment count to results (_comment_count field).
			join: Type of join for related tables (QB engine auto-determines optimal joins).
			distinct: Return only distinct results.
			start: Legacy alias for limit_start (deprecated).
			page_length: Legacy alias for limit_page_length (deprecated).
			ignore_ifnull: Skip IFNULL wrapping (QB engine handles NULL optimization automatically).
			save_user_settings: Save current query settings for user.
			save_user_settings_fields: Save field selection in user settings.
			update: Dictionary to merge into each result when as_list=False.
			user_settings: Custom user settings as JSON string or dict.
			reference_doctype: Reference doctype for contextual user permissions.
			run: Execute query immediately (True) or return query object (False).
			strict: Enable strict mode for query validation (legacy compatibility).
			pluck: Extract single field values as a simple list.
			ignore_ddl: Ignore DDL operations during query execution (legacy compatibility).
			parent_doctype: Parent doctype for child table queries.

		Returns:
			Query results as list of dicts (default) or list of lists (as_list=True).
			If pluck is specified, returns list of field values.
			If run=False, returns query object instead of results.

		Raises:
			ValidationError: For invalid parameters or query structure.
			PermissionError: When user lacks required permissions.
		"""

		# Check if table exists before running query (matching db_query behavior)
		from frappe.model.meta import get_table_columns

		try:
			get_table_columns(self.doctype)
		except frappe.db.TableMissingError:
			if ignore_ddl:
				return []
			else:
				raise

		# Handle deprecated parameters
		if limit_start:
			deprecation_warning(
				"2024-01-01", "v17", "The 'limit_start' parameter is deprecated. Use 'offset' instead."
			)
			if offset is None:
				offset = limit_start

		if limit_page_length:
			deprecation_warning(
				"2024-01-01", "v17", "The 'limit_page_length' parameter is deprecated. Use 'limit' instead."
			)
			if limit is None:
				limit = limit_page_length

		if start:
			deprecation_warning(
				"2024-01-01", "v17", "The 'start' parameter is deprecated. Use 'offset' instead."
			)
			if offset is None:
				offset = start

		if page_length:
			deprecation_warning(
				"2024-01-01", "v17", "The 'page_length' parameter is deprecated. Use 'limit' instead."
			)
			if limit is None:
				limit = page_length

		# filters and fields swappable
		# its hard to remember what comes first
		if isinstance(fields, dict) or (fields and isinstance(fields, list) and isinstance(fields[0], list)):
			# if fields is given as dict/list of list, its probably filters
			filters, fields = fields, filters

		elif fields and isinstance(filters, list) and len(filters) > 1 and isinstance(filters[0], str):
			# if `filters` is a list of strings, its probably fields
			filters, fields = fields, filters

		# Set fields to the requested field or `name` if none specified
		if not fields:
			fields = [pluck or "name"]

		# Build query using QB engine with converted syntax
		kwargs = {
			"table": self.doctype,
			"fields": fields,
			"filters": filters,
			"or_filters": or_filters,
			"group_by": group_by,
			"order_by": order_by,
			"limit": limit,
			"offset": offset,
			"distinct": distinct,
			"ignore_permissions": ignore_permissions,
			"user": user,
			"parent_doctype": parent_doctype,
			"reference_doctype": reference_doctype,
		}

		query = frappe.qb.get_query(**kwargs)

		if not run:
			# Return the SQL query string instead of executing
			return str(query.get_sql())

		# Run the query
		if pluck:
			result = query.run(debug=debug, as_dict=True, pluck=pluck)
		else:
			result = query.run(debug=debug, as_dict=not as_list, update=update)

		# Add comment count if requested and not as_list
		if with_comment_count and not as_list and self.doctype:
			self._add_comment_count(result)

		# Save user settings if requested
		if save_user_settings:
			user_settings_fields = copy.deepcopy(fields) if save_user_settings_fields else None

			if user_settings and isinstance(user_settings, str):
				user_settings = json.loads(user_settings)

			self._save_user_settings(user_settings, user_settings_fields, save_user_settings_fields)

		return result

	def _add_comment_count(self, result: list[Any]) -> None:
		"""Add comment count to each result row by parsing _comments field.

		This method adds a _comment_count field to each row based on the _comments field content.
		It parses the JSON structure to count the number of comments.

		Args:
			result: List of result dictionaries to modify
		"""
		if not result:
			return

		for row in result:
			if isinstance(row, dict) and "_comments" in row:
				try:
					comments_data = json.loads(row["_comments"] or "[]")
					row["_comment_count"] = len(comments_data) if isinstance(comments_data, list) else 0
				except (json.JSONDecodeError, TypeError):
					row["_comment_count"] = 0
			elif isinstance(row, dict):
				row["_comment_count"] = 0

	def _save_user_settings(
		self,
		user_settings: dict[str, Any] | None,
		user_settings_fields: list[str] | None,
		save_user_settings_fields: bool,
	) -> None:
		"""Save user settings for the current query.

		This method stores user preferences for field selections and other query parameters
		to provide a personalized experience for repeated queries.

		Args:
			user_settings: Custom user settings to save
			user_settings_fields: Field list to save if save_user_settings_fields is True
			save_user_settings_fields: Whether to save the field selection
		"""
		if not self.doctype:
			return

		try:
			current_settings = get_user_settings(self.doctype) or {}

			# Update with custom user settings if provided
			if user_settings:
				current_settings.update(user_settings)

			# Save field selection if requested
			if save_user_settings_fields and user_settings_fields:
				current_settings["fields"] = user_settings_fields

			# Only save if there are actual settings to save
			if current_settings:
				update_user_settings(self.doctype, current_settings)

		except Exception:
			# Don't let user settings errors break the query
			pass
