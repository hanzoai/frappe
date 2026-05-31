<template>
	<div v-if="shouldRender" class="builder-root">
		<PrintFormatControls />
		<div class="canvas-area">
			<!-- Sidebar-open hint -->
			<div v-if="sidebar_open && !hint_dismissed" class="pfb-sidebar-hint">
				<span v-html="frappe.utils.icon('sidebar', 'xs')"></span>
				<span>{{ __("Close the sidebar for more editing space") }}</span>
				<button class="pfb-hint-action" @click="close_desk_sidebar">
					{{ __("Close sidebar") }}
				</button>
				<button class="pfb-hint-dismiss" @click="dismiss_hint" :title="__('Dismiss')">
					<span v-html="frappe.utils.icon('x', 'xs')"></span>
				</button>
			</div>

			<!-- Canvas toolbar: sample data picker -->
			<div class="canvas-toolbar">
				<div class="canvas-toolbar-left">
					<span class="canvas-toolbar-eyebrow">{{ __("PREVIEW DATA") }}</span>
				</div>
				<div class="canvas-toolbar-center">
					<div ref="doc_picker_ref" class="canvas-doc-picker"></div>
				</div>
				<div class="canvas-toolbar-right">
					<span v-if="!$store.preview_doc.value" class="canvas-no-data-hint">
						← {{ __("Pick a record to see real values") }}
					</span>
					<button
						v-if="$store.preview_doc_name.value"
						class="canvas-clear-btn"
						:title="__('Clear preview data')"
						@click="clear_preview_doc"
						v-html="frappe.utils.icon('x', 'xs')"
					></button>
					<span v-if="$store.preview_doc.value" class="canvas-preview-badge">{{
						__("Live")
					}}</span>
				</div>
			</div>
			<div class="print-format-container" @click="clear_selection">
				<KeepAlive>
					<component :is="Preview" v-if="show_preview" />
					<component :is="PrintFormat" v-else />
				</KeepAlive>
			</div>
		</div>
		<FieldInspector v-if="!show_preview" />
	</div>
</template>

<script setup>
import PrintFormat from "./components/editor/PrintFormat.vue";
import Preview from "./components/Preview.vue";
import PrintFormatControls from "./components/PrintFormatControls.vue";
import FieldInspector from "./components/inspector/FieldInspector.vue";
import { getStore } from "./stores";
import { computed, ref, onMounted, onUnmounted, provide, nextTick } from "vue";

// props
const props = defineProps(["print_format_name"]);

const HINT_KEY = "pfb_sidebar_hint_dismissed";

// variables
let show_preview = ref(false);
let doc_picker_ref = ref(null);
let doc_picker_ctrl = ref(null);
let sidebar_open = ref(false);
let hint_dismissed = ref(localStorage.getItem(HINT_KEY) === "1");
let sidebar_observer = null;

// computed
let $store = computed(() => {
	return getStore(props.print_format_name);
});

let shouldRender = computed(() => {
	return Boolean(
		$store.value.print_format.value && $store.value.meta.value && $store.value.layout.value
	);
});

// provide
provide("$store", $store.value);

// methods
function toggle_preview() {
	show_preview.value = !show_preview.value;
}

function clear_selection() {
	$store.value.selected_field.value = null;
	$store.value.selected_section.value = null;
}

function handle_keydown(e) {
	if (e.key !== "Escape") return;
	// Don't intercept if a modal/dialog is open
	if (document.querySelector(".modal.show, .frappe-dialog:visible")) return;

	const sf = $store.value.selected_field.value;
	const ss = $store.value.selected_section.value;

	if (sf) {
		// Navigate up: field → parent section
		const lv = $store.value.layout.value;
		const all_sections = [lv?.header, ...(lv?.sections || []), lv?.footer].filter(Boolean);
		let parent = null;
		for (const sec of all_sections) {
			for (const col of sec.columns || []) {
				if (col.fields?.includes(sf)) {
					parent = sec;
					break;
				}
			}
			if (parent) break;
		}
		$store.value.selected_field.value = null;
		$store.value.selected_section.value = parent || null;
		e.stopPropagation();
	} else if (ss) {
		// Navigate up: section → canvas (clear all)
		$store.value.selected_section.value = null;
		e.stopPropagation();
	}
}

function check_sidebar() {
	const el = document.querySelector(".layout-side-section");
	sidebar_open.value = el ? el.offsetWidth > 0 : false;
}

function close_desk_sidebar() {
	// Frappe's desk sidebar toggle button
	const btn = document.querySelector(".sidebar-toggle-btn, [data-toggle='sidebar']");
	if (btn) {
		btn.click();
	} else {
		// Fallback: hide directly
		const el = document.querySelector(".layout-side-section");
		if (el) el.style.display = "none";
	}
	sidebar_open.value = false;
}

function dismiss_hint() {
	hint_dismissed.value = true;
	localStorage.setItem(HINT_KEY, "1");
}

function clear_preview_doc() {
	$store.value.load_preview_doc(null);
	doc_picker_ctrl.value?.set_value("");
}

function init_doc_picker() {
	if (!doc_picker_ref.value) return;
	const meta = $store.value.meta.value;
	doc_picker_ctrl.value = frappe.ui.form.make_control({
		parent: doc_picker_ref.value,
		df: {
			fieldname: "preview_doc",
			fieldtype: "Link",
			options: meta?.name,
			placeholder: __("Pick a {0} to preview...", [__(meta?.name || "document")]),
			change: () => {
				const name = doc_picker_ctrl.value.get_value();
				$store.value.load_preview_doc(name || null);
			},
		},
		render_input: true,
	});
	doc_picker_ref.value.querySelector(".control-label")?.remove();
	doc_picker_ref.value.querySelector(".form-group")?.style.setProperty("margin", "0");

	// Auto-select the first available record so preview is ready immediately
	frappe.db
		.get_list(meta?.name, { limit: 1, fields: ["name"], order_by: "creation desc" })
		.then((rows) => {
			if (rows?.length) {
				const first = rows[0].name;
				doc_picker_ctrl.value?.set_value(first);
				$store.value.load_preview_doc(first);
			}
		});
}

// mounted
onMounted(() => {
	document.addEventListener("keydown", handle_keydown);

	// Detect desk sidebar open/close via ResizeObserver
	check_sidebar();
	const sidebar_el = document.querySelector(".layout-side-section");
	if (sidebar_el) {
		sidebar_observer = new ResizeObserver(check_sidebar);
		sidebar_observer.observe(sidebar_el);
	}
	$store.value.fetch().then(() => {
		if (!$store.value.layout.value) {
			$store.value.layout.value = $store.value.get_default_layout();
			$store.value.save_changes();
		}
		nextTick(init_doc_picker);
	});
});

onUnmounted(() => {
	document.removeEventListener("keydown", handle_keydown);
	sidebar_observer?.disconnect();
});

defineExpose({ toggle_preview, $store });
</script>

<style scoped>
.builder-root {
	display: flex;
	width: 100%;
}

.canvas-area {
	flex: 1;
	min-width: 0;
	display: flex;
	flex-direction: column;
	height: calc(100vh - 95px);
}

/* ── Sidebar hint ────────────────────────────────────────── */
.pfb-sidebar-hint {
	flex-shrink: 0;
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 5px 14px;
	background: var(--yellow-50, #fefce8);
	border-bottom: 1px solid var(--yellow-200, #fde68a);
	font-size: var(--text-xs);
	color: var(--yellow-800, #854d0e);
}

.pfb-hint-action {
	margin-left: 2px;
	padding: 2px 8px;
	border: 1px solid var(--yellow-400, #facc15);
	border-radius: var(--border-radius-sm);
	background: transparent;
	color: var(--yellow-800, #854d0e);
	font-size: var(--text-xs);
	font-weight: 500;
	cursor: pointer;
	line-height: 1.4;
}

.pfb-hint-action:hover {
	background: var(--yellow-100, #fef9c3);
}

.pfb-hint-dismiss {
	margin-left: auto;
	display: flex;
	align-items: center;
	padding: 2px;
	border: none;
	background: transparent;
	cursor: pointer;
	color: var(--yellow-600, #ca8a04);
	border-radius: var(--border-radius-sm);
}

.pfb-hint-dismiss:hover {
	background: var(--yellow-100, #fef9c3);
}

/* ── Canvas toolbar ──────────────────────────────────────── */
.canvas-toolbar {
	flex-shrink: 0;
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 0 16px;
	height: 40px;
	border-bottom: 1px solid var(--border-color);
	background: var(--fg-color);
}

.canvas-toolbar-left {
	flex-shrink: 0;
}

.canvas-toolbar-eyebrow {
	font-size: 9px;
	font-weight: 700;
	letter-spacing: 0.1em;
	color: var(--text-muted);
	white-space: nowrap;
}

.canvas-toolbar-center {
	flex: 1;
	min-width: 0;
	max-width: 320px;
}

.canvas-doc-picker :deep(.form-group) {
	margin: 0;
}

.canvas-doc-picker :deep(.form-control) {
	font-size: var(--text-sm);
	height: 28px;
	padding: 2px 8px;
	border-radius: var(--border-radius);
}

.canvas-toolbar-right {
	flex-shrink: 0;
	display: flex;
	align-items: center;
	gap: 6px;
}

.canvas-no-data-hint {
	display: flex;
	align-items: center;
	gap: 4px;
	font-size: 11px;
	color: var(--text-muted);
	white-space: nowrap;
	background: var(--yellow-50, #fefce8);
	border: 1px solid var(--yellow-200, #fde68a);
	border-radius: var(--border-radius);
	padding: 3px 8px;
}

.canvas-clear-btn {
	display: flex;
	align-items: center;
	padding: 3px;
	border: none;
	background: transparent;
	cursor: pointer;
	color: var(--gray-400);
	border-radius: var(--border-radius-sm);
}

.canvas-clear-btn:hover {
	background: var(--gray-100);
	color: var(--gray-600);
}

.canvas-preview-badge {
	font-size: 10px;
	font-weight: 600;
	color: var(--green-600);
	background: var(--green-50);
	border: 1px solid var(--green-200);
	border-radius: var(--border-radius-sm);
	padding: 2px 6px;
	line-height: 1.4;
}

/* ── Canvas scroll area ──────────────────────────────────── */
.print-format-container {
	flex: 1;
	overflow-y: auto;
	padding-top: 0.5rem;
	padding-bottom: 4rem;
}
</style>
