// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("RQ Job", {
	refresh: function (frm) {
		// Nothing in this form is supposed to be editable.
		frm.disable_form();
		frm.dashboard.set_headline_alert(
<<<<<<< HEAD
			__("This is a virtual doctype and data is cleared periodically.")
=======
			"This is a virtual doctype and data is cleared periodically."
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		);

		if (["started", "queued"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Force Stop job"), () => {
				frappe.confirm(
<<<<<<< HEAD
					__(
						"This will terminate the job immediately and might be dangerous, are you sure? "
					),
=======
					"This will terminate the job immediately and might be dangerous, are you sure? ",
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
					() => {
						frappe
							.xcall("frappe.core.doctype.rq_job.rq_job.stop_job", {
								job_id: frm.doc.name,
							})
							.then((r) => {
<<<<<<< HEAD
								frappe.show_alert(__("Job Stopped Successfully"));
=======
								frappe.show_alert("Job Stopped Succefully");
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
								frm.reload_doc();
							});
					}
				);
			});
		}
	},
});
