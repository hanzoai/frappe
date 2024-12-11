# Copyright (c) 2015, Frappe Technologies and contributors
# License: MIT. See LICENSE

import json

import frappe
from frappe.model.document import Document
from frappe.translate import MERGED_TRANSLATION_KEY, USER_TRANSLATION_KEY
from frappe.utils import is_html, strip_html_tags


class Translation(Document):
<<<<<<< HEAD
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		context: DF.Data | None
		contributed: DF.Check
		contribution_docname: DF.Data | None
		contribution_status: DF.Literal["", "Pending", "Verified", "Rejected"]
		language: DF.Link
		source_text: DF.Code
		translated_text: DF.Code

	# end: auto-generated types
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	def validate(self):
		if is_html(self.source_text):
			self.remove_html_from_source()

	def remove_html_from_source(self):
		self.source_text = strip_html_tags(self.source_text).strip()

	def on_update(self):
		clear_user_translation_cache(self.language)

	def on_trash(self):
		clear_user_translation_cache(self.language)

<<<<<<< HEAD

def clear_user_translation_cache(lang):
	frappe.cache.hdel(USER_TRANSLATION_KEY, lang)
	frappe.cache.hdel(MERGED_TRANSLATION_KEY, lang)
=======
	def contribute(self):
		pass

	def get_contribution_status(self):
		pass


@frappe.whitelist()
def create_translations(translation_map, language):
	translation_map = json.loads(translation_map)
	translation_map_to_send = frappe._dict({})
	# first create / update local user translations
	for source_id, translation_dict in translation_map.items():
		translation_dict = frappe._dict(translation_dict)
		existing_doc_name = frappe.get_all(
			"Translation",
			{
				"source_text": translation_dict.source_text,
				"context": translation_dict.context or "",
				"language": language,
			},
		)
		translation_map_to_send[source_id] = translation_dict
		if existing_doc_name:
			frappe.db.set_value(
				"Translation",
				existing_doc_name[0].name,
				{
					"translated_text": translation_dict.translated_text,
					"contributed": 1,
					"contribution_status": "Pending",
				},
			)
			translation_map_to_send[source_id].name = existing_doc_name[0].name
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Translation",
					"source_text": translation_dict.source_text,
					"contributed": 1,
					"contribution_status": "Pending",
					"translated_text": translation_dict.translated_text,
					"context": translation_dict.context,
					"language": language,
				}
			)
			doc.insert()
			translation_map_to_send[source_id].name = doc.name


def clear_user_translation_cache(lang):
	frappe.cache().hdel(USER_TRANSLATION_KEY, lang)
	frappe.cache().hdel(MERGED_TRANSLATION_KEY, lang)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
