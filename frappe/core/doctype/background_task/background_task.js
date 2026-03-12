frappe.ui.form.on("Background Task", {
	refresh(frm) {
		frm.disable_save();

		if (frm.doc.status === "Running") {
			frm.dashboard.add_progress(__("Task Progress"), frm.doc.progress || 0);

			frm.task_update_handler = (data) => {
				if (data.task_id !== frm.doc.task_id) return;

				if (data.progress !== undefined) {
					frm.dashboard.add_progress(__("Task Progress"), data.progress);
				}
				if (data.stage) {
					frm.dashboard.set_headline(data.stage);
				}
				if (data.status && data.status !== "Running") {
					frappe.realtime.off("task_update", frm.task_update_handler);
					frm.reload_doc();
				}
			};

			frappe.realtime.on("task_update", frm.task_update_handler);
		}

		if (frm.doc.status === "Queued") {
			frm.dashboard.set_headline(__("Waiting for a worker to pick up this task..."));
		}
	},

	on_page_leave(frm) {
		if (frm.task_update_handler) {
			frappe.realtime.off("task_update", frm.task_update_handler);
			frm.task_update_handler = null;
		}
	},
});
