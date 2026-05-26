<template>
	<div v-if="shouldRender" class="builder-root">
		<PrintFormatControls />
		<div class="canvas-area">
			<!-- Canvas toolbar: sample data picker -->
			<div class="canvas-toolbar">
				<div class="canvas-toolbar-left">
					<span class="canvas-toolbar-eyebrow">{{ __("PREVIEW DATA") }}</span>
				</div>
				<div class="canvas-toolbar-center">
					<div ref="doc_picker_ref" class="canvas-doc-picker"></div>
				</div>
				<div class="canvas-toolbar-right">
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
import PrintFormat from "./PrintFormat.vue";
import Preview from "./Preview.vue";
import PrintFormatControls from "./PrintFormatControls.vue";
import FieldInspector from "./FieldInspector.vue";
import { getStore } from "./store";
import { computed, ref, onMounted, provide, nextTick } from "vue";

// props
const props = defineProps(["print_format_name"]);

// variables
let show_preview = ref(false);
let doc_picker_ref = ref(null);
let doc_picker_ctrl = ref(null);

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
}

// mounted
onMounted(() => {
	$store.value.fetch().then(() => {
		if (!$store.value.layout.value) {
			$store.value.layout.value = $store.value.get_default_layout();
			$store.value.save_changes();
		}
		nextTick(init_doc_picker);
	});
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
