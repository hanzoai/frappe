frappe.ui.form.on("Note", {
	refresh: function (frm) {
<<<<<<< HEAD
		if (!frm.is_new()) {
			frm.is_note_editable = false;
			frm.events.set_editable(frm);
		}
	},
	set_editable: function (frm) {
		if (frm.has_perm("write")) {
			const read_label = __("Read mode");
			const edit_label = __("Edit mode");
			frm.remove_custom_button(frm.is_note_editable ? edit_label : read_label);
			frm.add_custom_button(frm.is_note_editable ? read_label : edit_label, function () {
				frm.is_note_editable = !frm.is_note_editable;
				frm.events.set_editable(frm);
			});
		}
		// toggle "read_only" for content and "hidden" of all other fields

		// content read_only
		frm.set_df_property("content", "read_only", frm.is_note_editable ? 0 : 1);

		// hide all other fields
		for (const field of frm.meta.fields) {
			if (field.fieldname !== "content") {
				frm.set_df_property(
					field.fieldname,
					"hidden",
					frm.is_note_editable && !field.hidden && frm.get_perm(field.permlevel, "write")
						? 0
						: 1
				);
			}
		}

		// no label, description for content either
		frm.get_field("content").toggle_label(frm.is_note_editable);
		frm.get_field("content").toggle_description(frm.is_note_editable);
=======
		if (frm.doc.__islocal) {
			frm.events.set_editable(frm, true);
		} else {
			if (!frm.doc.content) {
				frm.doc.content = "<span></span>";
			}

			// toggle edit
			frm.add_custom_button("Edit", function () {
				frm.events.set_editable(frm, !frm.is_note_editable);
			});
			frm.events.set_editable(frm, false);
		}
	},
	set_editable: function (frm, editable) {
		// hide all fields other than content

		// no permission
		if (editable && !frm.perm[0].write) return;

		// content read_only
		frm.set_df_property("content", "read_only", editable ? 0 : 1);

		// hide all other fields
		$.each(frm.fields_dict, function (fieldname) {
			if (fieldname !== "content") {
				frm.set_df_property(fieldname, "hidden", editable ? 0 : 1);
			}
		});

		// no label, description for content either
		frm.get_field("content").toggle_label(editable);
		frm.get_field("content").toggle_description(editable);

		// set flag for toggle
		frm.is_note_editable = editable;
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	},
});

frappe.tour["Note"] = [
	{
		fieldname: "title",
		title: "Title of the Note",
		description: "This is the name by which the note will be saved, you can change this later",
	},
	{
		fieldname: "public",
		title: "Sets the Note to Public",
		description:
			"You can change the visibility of the note with this, setting it to public will allow other users to view it.",
	},
];
