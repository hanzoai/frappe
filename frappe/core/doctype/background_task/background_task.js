frappe.ui.form.on("Background Task", {
	refresh(frm) {
		frm.disable_save();

		if (frm.task_update_handler) {
			frappe.realtime.off("task_update", frm.task_update_handler);
			frm.task_update_handler = null;
		}

		if (!["Queued", "Running"].includes(frm.doc.status)) {
			return;
		}

		let stage_text = frm.doc.stage || "";
		if (frm.doc.status === "Queued") {
			stage_text = __("Waiting for a worker to pick up this task...");
		}
		if (stage_text) {
			frm.dashboard.set_headline(stage_text);
		}

		let progress_value = frm.doc.progress || 0;
		if (frm.doc.show_progress_bar !== 0) {
			frm.dashboard.show_progress(__("Task Progress"), progress_value);
		}

		let $bar = frm.dashboard.progress_area
			? frm.dashboard.progress_area.body.find(".progress-bar")
			: null;

		frm.task_update_handler = (data) => {
			if (data.task_id !== frm.doc.task_id) return;

			if (data.progress !== undefined && $bar) {
				$bar.css("width", data.progress + "%");
			}

			if (data.stage) {
				frm.dashboard.clear_headline();
				frm.dashboard.set_headline(data.stage);
			}

			if (data.status && data.status !== frm.doc.status) {
				frappe.realtime.off("task_update", frm.task_update_handler);
				frm.task_update_handler = null;
				frm.reload_doc();
			}
		};

		frappe.realtime.on("task_update", frm.task_update_handler);
	},

	on_page_leave(frm) {
		if (frm.task_update_handler) {
			frappe.realtime.off("task_update", frm.task_update_handler);
			frm.task_update_handler = null;
		}
	},
});
