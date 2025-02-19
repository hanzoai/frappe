import frappe
from frappe.permissions import handle_does_not_exist_error
from frappe.website.page_renderers.error_page import ErrorPage
from frappe.website.page_renderers.not_found_page import NotFoundPage
from frappe.website.page_renderers.not_permitted_page import NotPermittedPage
from frappe.website.page_renderers.redirect_page import RedirectPage
from frappe.website.path_resolver import PathResolver


def get_response(path=None, http_status_code=200):
	"""Resolves path and renders page"""
	path = path or frappe.local.request.path
	endpoint = path

	try:
		path_resolver = PathResolver(path)
		endpoint, renderer_instance = path_resolver.resolve()
		return renderer_instance.render()

	except Exception as e:
		return handle_exception(e, endpoint, path, http_status_code)


@handle_does_not_exist_error
def handle_exception(e, endpoint, path, http_status_code):
	if isinstance(e, frappe.Redirect):
		return RedirectPage(endpoint or path, http_status_code).render()

	if isinstance(e, frappe.PermissionError):
		return NotPermittedPage(endpoint, http_status_code, exception=e).render()

	if isinstance(e, frappe.PageDoesNotExistError):
		return NotFoundPage(endpoint, http_status_code).render()

	return ErrorPage(exception=e).render()


def get_response_content(path=None, http_status_code=200):
	response = get_response(path, http_status_code)
	return str(response.data, "utf-8")
