import frappe


class MaxFileSizeReachedError(frappe.ValidationError):
	pass


class FolderNotEmpty(frappe.ValidationError):
	pass


<<<<<<< HEAD
class FileTypeNotAllowed(frappe.ValidationError):
	pass


=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
from frappe.exceptions import *
