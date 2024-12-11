// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

<<<<<<< HEAD
if (frappe.require) {
	frappe.require("file_uploader.bundle.js");
} else {
	frappe.ready(function () {
		frappe.require("file_uploader.bundle.js");
	});
}
=======
import FileUploader from "./file_uploader";

frappe.provide("frappe.ui");
frappe.ui.FileUploader = FileUploader;
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
