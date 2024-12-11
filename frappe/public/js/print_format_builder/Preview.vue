<template>
	<div class="h-100">
		<div class="row">
			<div class="col">
<<<<<<< HEAD
				<div class="preview-control" ref="doc_select_ref"></div>
			</div>
			<div class="col">
				<div class="preview-control" ref="preview_type_ref"></div>
=======
				<div class="preview-control" ref="doc-select"></div>
			</div>
			<div class="col">
				<div class="preview-control" ref="preview-type"></div>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			</div>
			<div class="col d-flex">
				<a
					v-if="url"
					class="btn btn-default btn-sm btn-new-tab"
					target="_blank"
					:href="url"
				>
					{{ __("Open in a new tab") }}
				</a>
				<button
					v-if="url"
					class="ml-3 btn btn-default btn-sm btn-new-tab"
					@click="refresh"
				>
					{{ __("Refresh") }}
				</button>
			</div>
		</div>
		<div v-if="url && !preview_loaded">Generating preview...</div>
		<iframe
			ref="iframe"
			:src="url"
			v-if="url"
			v-show="preview_loaded"
			class="preview-iframe"
			@load="preview_loaded = true"
		></iframe>
	</div>
</template>
<<<<<<< HEAD

<script setup>
import { useStore } from "./store";
import { ref, computed, onMounted } from "vue";

// mixin
let { print_format, store } = useStore();

// variables
let type = ref("PDF");
let docname = ref(null);
let preview_loaded = ref(false);
let iframe = ref(null);
let doc_select_ref = ref(null);
let preview_type_ref = ref(null);
let doc_select = ref(null);
let preview_type = ref(null);

// methods
function refresh() {
	iframe.value?.contentWindow.location.reload();
}
function get_default_docname() {
	return frappe.db.get_list(doctype.value, { limit: 1 }).then((doc) => {
		return doc.length > 0 ? doc[0].name : null;
	});
}
// computed
let doctype = computed(() => {
	return print_format.value.doc_type;
});
let url = computed(() => {
	if (!docname.value) return null;
	let params = new URLSearchParams();
	params.append("doctype", doctype.value);
	params.append("name", docname.value);
	params.append("print_format", print_format.value.name);

	if (store.value.letterhead) {
		params.append("letterhead", store.value.letterhead.name);
	}
	let _url =
		type.value == "PDF" ? `/api/method/frappe.utils.weasyprint.download_pdf` : "/printpreview";
	return `${_url}?${params.toString()}`;
});

// mounted
onMounted(() => {
	doc_select.value = frappe.ui.form.make_control({
		parent: doc_select_ref.value,
		df: {
			label: __("Select {0}", [__(doctype.value)]),
			fieldname: "docname",
			fieldtype: "Link",
			options: doctype.value,
			change: () => {
				docname.value = doc_select.value.get_value();
			},
		},
		render_input: true,
	});
	preview_type.value = frappe.ui.form.make_control({
		parent: preview_type_ref.value,
		df: {
			label: __("Preview type"),
			fieldname: "docname",
			fieldtype: "Select",
			options: ["PDF", "HTML"],
			change: () => {
				type.value = preview_type.value.get_value();
			},
		},
		render_input: true,
	});
	preview_type.value.set_value(type.value);
	get_default_docname().then((doc_name) => {
		doc_name && doc_select.value.set_value(doc_name);
	});
});
</script>

=======
<script>
import { storeMixin } from "./store";
export default {
	name: "Preview",
	mixins: [storeMixin],
	data() {
		return {
			type: "PDF",
			docname: null,
			preview_loaded: false,
		};
	},
	mounted() {
		this.doc_select = frappe.ui.form.make_control({
			parent: this.$refs["doc-select"],
			df: {
				label: __("Select {0}", [__(this.doctype)]),
				fieldname: "docname",
				fieldtype: "Link",
				options: this.doctype,
				change: () => {
					this.docname = this.doc_select.get_value();
				},
			},
			render_input: true,
		});
		this.preview_type = frappe.ui.form.make_control({
			parent: this.$refs["preview-type"],
			df: {
				label: __("Preview type"),
				fieldname: "docname",
				fieldtype: "Select",
				options: ["PDF", "HTML"],
				change: () => {
					this.type = this.preview_type.get_value();
				},
			},
			render_input: true,
		});
		this.preview_type.set_value(this.type);
		this.get_default_docname().then(
			(docname) => docname && this.doc_select.set_value(docname)
		);
		this.$store.$on("after_save", () => {
			this.refresh();
		});
	},
	methods: {
		refresh() {
			this.$refs.iframe.contentWindow.location.reload();
		},
		get_default_docname() {
			return frappe.db.get_list(this.doctype, { limit: 1 }).then((doc) => {
				return doc.length > 0 ? doc[0].name : null;
			});
		},
	},
	computed: {
		doctype() {
			return this.print_format.doc_type;
		},
		url() {
			if (!this.docname) return null;
			let params = new URLSearchParams();
			params.append("doctype", this.doctype);
			params.append("name", this.docname);
			params.append("print_format", this.print_format.name);
			if (this.$store.letterhead) {
				params.append("letterhead", this.$store.letterhead.name);
			}
			let url =
				this.type == "PDF"
					? `/api/method/frappe.utils.weasyprint.download_pdf`
					: "/printpreview";
			return `${url}?${params.toString()}`;
		},
	},
};
</script>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
<style scoped>
.preview-iframe {
	width: 100%;
	height: 96%;
	border: none;
	border-radius: var(--border-radius);
}
.btn-new-tab {
	margin-top: auto;
	margin-bottom: 1.2rem;
}
.preview-control :deep(.form-control) {
	background: var(--control-bg-on-gray);
}
</style>
