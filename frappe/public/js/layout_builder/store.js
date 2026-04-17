import { defineStore } from "pinia";
import { ref, computed } from "vue";

// Field properties that can be overridden per layout
export const OVERRIDE_PROPS = [
	{ fieldname: "label", label: "Label", fieldtype: "Data", description: "Override the field label for this layout" },
	{ fieldname: "hidden", label: "Hidden", fieldtype: "Check", description: "Hide this field in the layout" },
	{ fieldname: "reqd", label: "Required", fieldtype: "Check", description: "Make this field mandatory in the layout" },
	{ fieldname: "read_only", label: "Read Only", fieldtype: "Check", description: "Make this field read-only in the layout" },
	{ fieldname: "allow_in_quick_entry", label: "Allow in Quick Entry", fieldtype: "Check" },
	{ fieldname: "bold", label: "Bold", fieldtype: "Check" },
	{ fieldname: "in_list_view", label: "In List View", fieldtype: "Check" },
	{ fieldname: "in_standard_filter", label: "In Standard Filter", fieldtype: "Check" },
	{ fieldname: "default", label: "Default Value", fieldtype: "Data", description: "Override the default value" },
	{ fieldname: "description", label: "Description", fieldtype: "Small Text", description: "Override the field description" },
	{ fieldname: "depends_on", label: "Depends On", fieldtype: "Data", description: "eval: doc.field == 'x'" },
	{ fieldname: "mandatory_depends_on", label: "Mandatory Depends On", fieldtype: "Data" },
	{ fieldname: "read_only_depends_on", label: "Read Only Depends On", fieldtype: "Data" },
];

// The subset that apply only to non-structural fields
export const STRUCTURAL_TYPES = new Set(["Section Break", "Column Break", "Tab Break"]);

export const useLayoutBuilderStore = defineStore("layout-builder-store", () => {
	/** The Frappe frm object for the DocType Layout document */
	let frm = ref(null);
	/** doctype_layout doc (frm.doc) */
	let doc = ref(null);
	/** The flat list of layout field rows (frm.doc.fields) rendered in order */
	let fields = ref([]);
	/** Currently selected field row (DocType Layout Field row object) */
	let selected_field = ref(null);
	/** Whether any unsaved changes exist */
	let dirty = ref(false);

	// ── Computed ────────────────────────────────────────────────────────────────

	/** docfield_map for the parent DocType, keyed by fieldname */
	let base_meta = computed(() => {
		if (!doc.value?.document_type) return {};
		return frappe.meta.docfield_map[doc.value.document_type] || {};
	});

	// ── Actions ──────────────────────────────────────────────────────────────────

	function init(_frm) {
		frm.value = _frm;
		doc.value = _frm.doc;
		reload();
	}

	/** Re-read from frm.doc.fields (called after sync or after_save) */
	function reload() {
		fields.value = (frm.value.doc.fields || []).slice().sort((a, b) => a.idx - b.idx);
		selected_field.value = null;
		dirty.value = false;
	}

	function select(field_row) {
		selected_field.value = field_row;
	}

	function deselect() {
		selected_field.value = null;
	}

	/** Write a property change on the selected/given layout field row back into frm.doc */
	function update_field(fieldname, prop, value) {
		const row = (frm.value.doc.fields || []).find((f) => f.fieldname === fieldname);
		if (!row) return;
		row[prop] = value;
		// also update the reactive copy in fields[]
		const reactive_row = fields.value.find((f) => f.fieldname === fieldname);
		if (reactive_row) reactive_row[prop] = value;
		mark_dirty();
	}

	/** Reorder frm.doc.fields to match the current drag-drop order in fields[] */
	function reorder(new_order_fieldnames) {
		const by_name = {};
		(frm.value.doc.fields || []).forEach((f) => { by_name[f.fieldname] = f; });
		frm.value.doc.fields = new_order_fieldnames.map((fn, i) => {
			const f = by_name[fn];
			if (f) f.idx = i + 1;
			return f;
		}).filter(Boolean);
		// keep fields[] in sync
		fields.value = frm.value.doc.fields.slice();
		mark_dirty();
	}

	function mark_dirty() {
		dirty.value = true;
		frm.value.dirty();
	}

	return {
		frm, doc, fields, selected_field, dirty,
		base_meta,
		init, reload, select, deselect, update_field, reorder, mark_dirty,
	};
});
