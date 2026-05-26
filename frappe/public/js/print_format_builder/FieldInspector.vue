<template>
	<div class="pfb-inspector" @click.stop>
		<!-- Header -->
		<div class="pfb-inspector-head">
			<div class="pfb-inspector-eyebrow">{{ __("Inspector") }}</div>
			<div class="pfb-inspector-title">
				<span class="pfb-inspector-kind">{{
					selected_field ? __("Field") : __("Canvas")
				}}</span>
				<span class="pfb-inspector-name text-muted" v-if="selected_field">
					{{ selected_field.label || selected_field.fieldname }}
				</span>
			</div>
		</div>

		<!-- Empty state -->
		<div v-if="!selected_field" class="pfb-inspector-empty">
			<svg class="icon icon-md text-muted" style="margin-bottom: 8px">
				<use href="#icon-cursor-text"></use>
			</svg>
			<p class="text-muted">{{ __("Click a field to edit its properties") }}</p>
		</div>

		<!-- Field properties -->
		<template v-else>
			<!-- Section: Field -->
			<div class="pfb-insp-section">
				<div class="pfb-insp-section-label">{{ __("Field") }}</div>

				<!-- Source (read-only) -->
				<div class="pfb-insp-row">
					<span class="pfb-insp-label">{{ __("Source") }}</span>
					<div class="pfb-source-display">
						<span class="pfb-source-name">
							{{ selected_field.label || selected_field.fieldname }}
						</span>
						<span class="fieldtype-badge">{{ short_fieldtype }}</span>
					</div>
				</div>

				<!-- Label -->
				<div class="pfb-insp-row pfb-insp-row--full">
					<span class="pfb-insp-label">{{ __("Label") }}</span>
					<input
						class="form-control form-control-sm"
						type="text"
						:placeholder="__('Field label')"
						v-model="selected_field.label"
					/>
				</div>

				<!-- Show label -->
				<div class="pfb-insp-row">
					<span class="pfb-insp-label">{{ __("Show label") }}</span>
					<div class="pfb-seg">
						<button
							v-for="opt in show_label_opts"
							:key="opt.value"
							:class="{ active: current_show_label === opt.value }"
							@click="selected_field.show_label = opt.value"
						>
							{{ opt.label }}
						</button>
					</div>
				</div>

				<!-- Align -->
				<div class="pfb-insp-row">
					<span class="pfb-insp-label">{{ __("Align") }}</span>
					<div class="pfb-seg">
						<button
							v-for="opt in align_opts"
							:key="opt.value"
							:class="{ active: current_align === opt.value }"
							:title="opt.title"
							@click="selected_field.align = opt.value"
							v-html="opt.icon"
						></button>
					</div>
				</div>
			</div>

			<!-- Section: remove -->
			<div class="pfb-insp-section pfb-insp-section--actions">
				<button class="btn btn-xs btn-danger-subtle" @click="remove_field">
					<span v-html="frappe.utils.icon('x', 'xs')"></span>
					{{ __("Remove field") }}
				</button>
			</div>
		</template>
	</div>
</template>

<script setup>
import { computed, inject } from "vue";

let store = inject("$store");

let selected_field = computed(() => store.selected_field.value);

let short_fieldtype = computed(() => {
	if (!selected_field.value) return "";
	const map = {
		Data: "Data",
		Currency: "Currency",
		Int: "Int",
		Float: "Float",
		Date: "Date",
		Datetime: "DateTime",
		Check: "Check",
		Select: "Select",
		Table: "Table",
		"Long Text": "Text",
		Text: "Text",
		Link: "Link",
		HTML: "HTML",
		Spacer: "Spacer",
		Divider: "Divider",
		"Field Template": "Template",
	};
	return map[selected_field.value.fieldtype] || selected_field.value.fieldtype || "";
});

let current_show_label = computed(() => selected_field.value?.show_label ?? "show");
let current_align = computed(() => selected_field.value?.align ?? "left");

const show_label_opts = [
	{ value: "show", label: __("Show") },
	{ value: "hide", label: __("Hide") },
	{ value: "inline", label: __("Inline") },
];

const align_icons = {
	left: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="12" viewBox="0 0 14 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="0" y1="1" x2="14" y2="1"/><line x1="0" y1="5" x2="9" y2="5"/><line x1="0" y1="9" x2="11" y2="9"/></svg>`,
	center: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="12" viewBox="0 0 14 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="0" y1="1" x2="14" y2="1"/><line x1="2.5" y1="5" x2="11.5" y2="5"/><line x1="1.5" y1="9" x2="12.5" y2="9"/></svg>`,
	right: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="12" viewBox="0 0 14 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="0" y1="1" x2="14" y2="1"/><line x1="5" y1="5" x2="14" y2="5"/><line x1="3" y1="9" x2="14" y2="9"/></svg>`,
};

const align_opts = [
	{ value: "left", title: __("Align left"), icon: align_icons.left },
	{ value: "center", title: __("Align center"), icon: align_icons.center },
	{ value: "right", title: __("Align right"), icon: align_icons.right },
];

function remove_field() {
	if (selected_field.value) {
		selected_field.value.remove = true;
		store.selected_field.value = null;
	}
}
</script>

<style scoped>
.pfb-inspector {
	width: 260px;
	flex-shrink: 0;
	height: calc(100vh - 95px);
	overflow-y: auto;
	border-left: 1px solid var(--border-color);
	background: var(--fg-color);
	display: flex;
	flex-direction: column;
}

/* ── Header ─────────────────────────────────────────────── */
.pfb-inspector-head {
	padding: 12px 12px 10px;
	border-bottom: 1px solid var(--border-color);
	flex-shrink: 0;
}

.pfb-inspector-eyebrow {
	font-size: 10px;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: var(--text-muted);
	margin-bottom: 2px;
}

.pfb-inspector-title {
	display: flex;
	align-items: baseline;
	gap: 6px;
}

.pfb-inspector-kind {
	font-size: var(--text-base);
	font-weight: 600;
}

.pfb-inspector-name {
	font-size: var(--text-sm);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

/* ── Empty state ─────────────────────────────────────────── */
.pfb-inspector-empty {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 24px;
	text-align: center;
	font-size: var(--text-sm);
}

/* ── Sections ────────────────────────────────────────────── */
.pfb-insp-section {
	padding: 12px;
	border-bottom: 1px solid var(--border-color);
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.pfb-insp-section-label {
	font-size: 10px;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: var(--text-muted);
}

/* ── Rows ────────────────────────────────────────────────── */
.pfb-insp-row {
	display: grid;
	grid-template-columns: 72px 1fr;
	align-items: center;
	gap: 8px;
}

.pfb-insp-row--full {
	grid-template-columns: 1fr;
	gap: 4px;
}

.pfb-insp-label {
	font-size: var(--text-sm);
	color: var(--text-muted);
}

/* ── Source display ──────────────────────────────────────── */
.pfb-source-display {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 4px 8px;
	border: 1px solid var(--border-color);
	border-radius: var(--border-radius);
	background: var(--gray-50);
	gap: 6px;
}

.pfb-source-name {
	font-size: var(--text-sm);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.fieldtype-badge {
	font-size: 10px;
	color: var(--text-muted);
	background: var(--gray-100);
	border: 1px solid var(--gray-300);
	border-radius: var(--border-radius-sm);
	padding: 1px 5px;
	white-space: nowrap;
	flex-shrink: 0;
}

/* ── Segmented control ───────────────────────────────────── */
.pfb-seg {
	display: inline-flex;
	background: var(--gray-100);
	border: 1px solid var(--border-color);
	border-radius: var(--border-radius);
	overflow: hidden;
	width: 100%;
}

.pfb-seg button {
	flex: 1;
	padding: 4px 6px;
	font-size: 11px;
	font-weight: 500;
	border: none;
	border-radius: 0;
	background: transparent;
	color: var(--text-muted);
	cursor: pointer;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	line-height: 1;
}

.pfb-seg button:not(:first-child) {
	border-left: 1px solid var(--border-color);
}

.pfb-seg button:hover {
	background: var(--gray-200);
	color: var(--text-color);
}

.pfb-seg button.active {
	background: var(--fg-color);
	color: var(--text-color);
	box-shadow: var(--shadow-xs);
}

/* ── Actions ─────────────────────────────────────────────── */
.pfb-insp-section--actions {
	margin-top: auto;
	border-bottom: none;
	border-top: 1px solid var(--border-color);
}

.btn-danger-subtle {
	display: inline-flex;
	align-items: center;
	gap: 4px;
	color: var(--red-500);
	background: transparent;
	border: 1px solid var(--red-200);
	border-radius: var(--border-radius);
	padding: 4px 8px;
	font-size: var(--text-sm);
	cursor: pointer;
}

.btn-danger-subtle:hover {
	background: var(--red-50);
	border-color: var(--red-300);
}
</style>
