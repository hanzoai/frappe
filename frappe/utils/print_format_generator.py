# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE

from typing import ClassVar

import frappe
from frappe import _


@frappe.whitelist()
def download_pdf(doctype: str, name: str | int, print_format: str, letterhead: str | None = None):
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("print")
	generator = PrintFormatGenerator(print_format, doc, letterhead)
	pdf = generator.render_pdf()

	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = pdf
	frappe.local.response.type = "pdf"


def get_html(doctype, name, print_format, letterhead=None):
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("print")
	generator = PrintFormatGenerator(print_format, doc, letterhead)
	return generator.get_html_preview()


class PrintFormatGenerator:
	"""Generate a PDF of a Document using Chromium-based rendering."""

	def __init__(self, print_format, doc, letterhead=None):
		self.print_format = frappe.get_doc("Print Format", print_format)
		self.doc = doc

		if letterhead == _("No Letterhead"):
			letterhead = None
		self.letterhead = frappe.get_doc("Letter Head", letterhead) if letterhead else None

		self.build_context()
		self.layout = self.get_layout(self.print_format)
		self.context.layout = self.layout

	def build_context(self):
		self.print_settings = frappe.get_doc("Print Settings")
		page_width_map = {"A4": 210, "Letter": 216}
		page_width = page_width_map.get(self.print_settings.pdf_page_size) or 210
		body_width = page_width - self.print_format.margin_left - self.print_format.margin_right
		print_style = (
			frappe.get_doc("Print Style", self.print_settings.print_style)
			if self.print_settings.print_style
			else None
		)
		self.context = frappe._dict(
			{
				"doc": self.doc,
				"print_format": self.print_format,
				"print_settings": self.print_settings,
				"print_style": print_style,
				"letterhead": self.letterhead,
				"page_width": page_width,
				"body_width": body_width,
			}
		)

	def get_html_preview(self):
		header_html, footer_html = self.get_header_footer_html()
		self.context.header = header_html
		self.context.footer = footer_html
		return self.get_main_html()

	def get_main_html(self):
		self.context.css = frappe.render_template("templates/print_format/print_format.css", self.context)
		return frappe.render_template("templates/print_format/print_format.html", self.context)

	def get_header_footer_html(self):
		header_html = footer_html = None
		if self.letterhead or self.layout.get("header"):
			header_html = frappe.render_template("templates/print_format/print_header.html", self.context)
		if self.letterhead or self.layout.get("footer"):
			footer_html = frappe.render_template("templates/print_format/print_footer.html", self.context)
		return header_html, footer_html

	def render_pdf(self):
		"""Return PDF bytes using Chromium renderer."""
		from frappe.utils.pdf import get_chrome_pdf

		html = self._build_html_for_chrome()
		options = self._get_margin_options()
		return get_chrome_pdf(
			print_format=self.print_format.name,
			html=html,
			options=options,
			output=None,
			pdf_generator="chrome",
		)

	_TOP_POSITIONS: ClassVar[set[str]] = {"top_left", "top_center", "top_right"}
	_BOTTOM_POSITIONS: ClassVar[set[str]] = {"bottom_left", "bottom_center", "bottom_right"}
	_ALIGN_MAP: ClassVar[dict[str, str]] = {
		"top_left": "left",
		"top_center": "center",
		"top_right": "right",
		"bottom_left": "left",
		"bottom_center": "center",
		"bottom_right": "right",
	}

	def _build_html_for_chrome(self):
		"""Build HTML for Chrome rendering.

		When repeat_header_footer is on: wrap header/footer in #header-html / #footer-html so
		Chrome extracts them as overlay pages shown on every page.
		When off: render them inline so they appear as body content (first/last page only).
		Page numbers are only supported in overlay mode; inline mode omits them.
		"""
		self.context.for_chrome = True
		self.context.header_height = 0
		self.context.footer_height = 0

		# Always use overlay mode for print_format_builder_beta so the header/footer
		# repeat on every page, regardless of the global "Repeat Header and Footer" setting.
		repeat = 1

		header = self._render_chrome_header(with_page_number=repeat)
		footer = self._render_chrome_footer(with_page_number=repeat)

		if repeat:
			self.context.header = f'<div id="header-html">{header}</div>' if header else ""
			self.context.footer = f'<div id="footer-html">{footer}</div>' if footer else ""
		else:
			# Inline: shows on first page (header) and last page (footer) naturally
			self.context.header = header or ""
			self.context.footer = footer or ""

		return self.get_main_html()

	def _page_number_html(self, position):
		align = self._ALIGN_MAP.get(position, "center")
		return (
			f'<div style="text-align:{align};font-size:10px;padding:2px 0;">'
			'<span class="page"></span>'
			f" {_('of')} "
			'<span class="topage"></span>'
			"</div>"
		)

	def _render_chrome_header(self, with_page_number=True):
		"""Render header content for Chrome (no position:fixed CSS)."""
		page_pos = (self.print_format.page_number or "").lower().replace(" ", "_")
		wants_page_no = with_page_number and page_pos in self._TOP_POSITIONS
		has_content = self.letterhead or self.layout.get("header")

		if not has_content and not wants_page_no:
			return None

		parts = []
		# Page number goes FIRST in the header so "Top Left/Center/Right" actually
		# renders above the letterhead and document-header, not squeezed underneath.
		if wants_page_no:
			parts.append(self._page_number_html(page_pos))
		if self.letterhead and self.letterhead.content:
			parts.append(frappe.render_template(self.letterhead.content, {"doc": self.context.doc}))
		if self.layout.get("header"):
			parts.append(frappe.render_template(self.layout["header"], {"doc": self.context.doc}))
		return "\n".join(parts) or None

	def _render_chrome_footer(self, with_page_number=True):
		"""Render footer content for Chrome (no position:fixed CSS)."""
		page_pos = (self.print_format.page_number or "").lower().replace(" ", "_")
		wants_page_no = with_page_number and page_pos in self._BOTTOM_POSITIONS
		has_content = self.layout.get("footer") or (self.letterhead and self.letterhead.footer)

		if not has_content and not wants_page_no:
			return None

		parts = []
		if self.layout.get("footer"):
			parts.append(frappe.render_template(self.layout["footer"], {"doc": self.context.doc}))
		if self.letterhead and self.letterhead.footer:
			parts.append(frappe.render_template(self.letterhead.footer, {"doc": self.context.doc}))
		if wants_page_no:
			parts.append(self._page_number_html(page_pos))
		return "\n".join(parts) or None

	def _get_margin_options(self):
		pf = self.print_format
		return {
			"margin-top": f"{pf.margin_top}mm",
			"margin-bottom": f"{pf.margin_bottom}mm",
			"margin-left": f"{pf.margin_left}mm",
			"margin-right": f"{pf.margin_right}mm",
		}

	def get_layout(self, print_format):
		layout = frappe.parse_json(print_format.format_data)
		layout = self.set_field_renderers(layout)
		layout = self.process_margin_texts(layout)
		return layout

	def set_field_renderers(self, layout):
		renderers = {"HTML Editor": "HTML", "Markdown Editor": "Markdown"}
		for section in layout["sections"]:
			for column in section["columns"]:
				for df in column["fields"]:
					fieldtype = df["fieldtype"]
					df["renderer"] = renderers.get(fieldtype) or fieldtype.replace(" ", "")
					df["section"] = section
		return layout

	def process_margin_texts(self, layout):
		margin_text_keys = [
			"top_left",
			"top_center",
			"top_right",
			"bottom_left",
			"bottom_center",
			"bottom_right",
		]
		for key in margin_text_keys:
			text = layout.get("text_" + key)
			if text and "{{" in text:
				layout["text_" + key] = frappe.render_template(text, self.context)
		return layout
