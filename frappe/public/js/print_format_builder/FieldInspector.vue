<template>
	<div class="pfb-inspector" @click.stop>
		<!-- Header -->
		<div class="pfb-inspector-head">
			<div class="pfb-inspector-eyebrow">{{ __("Inspector") }}</div>
			<div class="pfb-inspector-title-row">
				<div class="pfb-inspector-title">
					<span class="pfb-inspector-kind">{{
						selected_field ? __("Field") : __("Canvas")
					}}</span>
					<span class="pfb-inspector-name" v-if="selected_field">
						{{ selected_field.label || selected_field.fieldname }}
					</span>
				</div>
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
			<!-- Tab bar -->
			<div class="pfb-insp-tabs">
				<button
					v-for="tab in inspector_tabs"
					:key="tab.id"
					class="pfb-insp-tab"
					:class="{ active: activeInspectorTab === tab.id }"
					@click="activeInspectorTab = tab.id"
				>
					{{ tab.label }}
				</button>
			</div>

			<!-- Properties tab -->
			<div v-if="activeInspectorTab === 'properties'" class="pfb-insp-body">
				<!-- FIELD section -->
				<div class="pfb-insp-section">
					<div class="pfb-insp-section-head" @click="toggle_section('field')">
						<span class="pfb-insp-section-label">{{ __("Field") }}</span>
						<span
							class="pfb-insp-chevron"
							:class="{ collapsed: !sections_open.field }"
							v-html="frappe.utils.icon('chevron-down', 'xs')"
						></span>
					</div>

					<div v-show="sections_open.field" class="pfb-insp-section-body">
						<!-- Source (read-only) -->
						<div class="pfb-insp-row">
							<span class="pfb-insp-label">{{ __("Source") }}</span>
							<div class="pfb-source-display">
								<span class="pfb-source-name">
									{{ selected_field.label || selected_field.fieldname }}
								</span>
								<span class="pfb-type-badge">{{ short_fieldtype }}</span>
							</div>
						</div>

						<!-- Label -->
						<div class="pfb-insp-row pfb-insp-row--col">
							<span class="pfb-insp-label">{{ __("Label") }}</span>
							<input
								class="pfb-insp-input"
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
				</div>

				<!-- FORMAT section -->
				<div class="pfb-insp-section">
					<div class="pfb-insp-section-head" @click="toggle_section('format')">
						<span class="pfb-insp-section-label">{{ __("Format") }}</span>
						<span
							class="pfb-insp-chevron"
							:class="{ collapsed: !sections_open.format }"
							v-html="frappe.utils.icon('chevron-down', 'xs')"
						></span>
					</div>
					<div v-show="sections_open.format" class="pfb-insp-section-body">
						<p class="pfb-insp-hint text-muted">
							{{ __("Additional formatting options coming soon.") }}
						</p>
					</div>
				</div>

				<!-- VISIBILITY section -->
				<div class="pfb-insp-section">
					<div class="pfb-insp-section-head" @click="toggle_section('visibility')">
						<span class="pfb-insp-section-label">{{ __("Visibility") }}</span>
						<span
							class="pfb-insp-chevron"
							:class="{ collapsed: !sections_open.visibility }"
							v-html="frappe.utils.icon('chevron-down', 'xs')"
						></span>
					</div>
					<div v-show="sections_open.visibility" class="pfb-insp-section-body">
						<p class="pfb-insp-hint text-muted">
							{{ __("Conditional visibility coming soon.") }}
						</p>
					</div>
				</div>

				<!-- Actions -->
				<div class="pfb-insp-actions">
					<button class="btn btn-xs btn-danger-subtle" @click="remove_field">
						<span v-html="frappe.utils.icon('x', 'xs')"></span>
						{{ __("Remove field") }}
					</button>
				</div>
			</div>

			<!-- Style tab (placeholder) -->
			<div
				v-else-if="activeInspectorTab === 'style'"
				class="pfb-insp-body pfb-insp-placeholder"
			>
				<p class="text-muted">{{ __("Style overrides coming soon.") }}</p>
			</div>

			<!-- Logic tab (placeholder) -->
			<div
				v-else-if="activeInspectorTab === 'logic'"
				class="pfb-insp-body pfb-insp-placeholder"
			>
				<p class="text-muted">{{ __("Conditional logic coming soon.") }}</p>
			</div>
		</template>
	</div>
</template>

<script setup>
import { computed, inject, ref } from "vue";

let store = inject("$store");

let selected_field = computed(() => store.selected_field.value);
let activeInspectorTab = ref("properties");

const inspector_tabs = [
	{ id: "properties", label: __("Properties") },
	{ id: "style", label: __("Style") },
	{ id: "logic", label: __("Logic") },
];

const sections_open = ref({ field: true, format: false, visibility: false });

function toggle_section(name) {
	sections_open.value[name] = !sections_open.value[name];
}

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
	width: 280px;
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
	padding: 12px 14px 10px;
	border-bottom: 1px solid var(--border-color);
	flex-shrink: 0;
}

.pfb-inspector-eyebrow {
	font-size: 10px;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: var(--text-muted);
	margin-bottom: 3px;
}

.pfb-inspector-title {
	display: flex;
	align-items: baseline;
	gap: 6px;
}

.pfb-inspector-kind {
	font-size: var(--text-lg);
	font-weight: 700;
}

.pfb-inspector-name {
	font-size: var(--text-base);
	color: var(--text-muted);
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

/* ── Inspector tabs ──────────────────────────────────────── */
.pfb-insp-tabs {
	display: flex;
	padding: 8px 10px 0;
	gap: 2px;
	border-bottom: 1px solid var(--border-color);
	flex-shrink: 0;
	background: var(--gray-50);
}

.pfb-insp-tab {
	flex: 1;
	padding: 6px 4px 8px;
	font-size: var(--text-sm);
	font-weight: 500;
	border: none;
	background: transparent;
	color: var(--text-muted);
	cursor: pointer;
	border-radius: var(--border-radius) var(--border-radius) 0 0;
	position: relative;
	transition: color 0.12s;
}

.pfb-insp-tab:hover {
	color: var(--text-color);
}

.pfb-insp-tab.active {
	color: var(--text-color);
	font-weight: 600;
}

.pfb-insp-tab.active::after {
	content: "";
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	height: 2px;
	background: var(--gray-700);
	border-radius: 2px 2px 0 0;
}

/* ── Inspector body ──────────────────────────────────────── */
.pfb-insp-body {
	flex: 1;
	overflow-y: auto;
	display: flex;
	flex-direction: column;
}

/* ── Collapsible sections ────────────────────────────────── */
.pfb-insp-section {
	border-bottom: 1px solid var(--border-color);
}

.pfb-insp-section-head {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 10px 14px;
	cursor: pointer;
	user-select: none;
}

.pfb-insp-section-head:hover {
	background: var(--gray-50);
}

.pfb-insp-section-label {
	font-size: 10px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: var(--text-muted);
}

.pfb-insp-chevron {
	display: flex;
	align-items: center;
	color: var(--gray-400);
	transition: transform 0.15s;
}

.pfb-insp-chevron.collapsed {
	transform: rotate(-90deg);
}

.pfb-insp-section-body {
	padding: 4px 14px 12px;
	display: flex;
	flex-direction: column;
	gap: 10px;
}

/* ── Rows ────────────────────────────────────────────────── */
.pfb-insp-row {
	display: grid;
	grid-template-columns: 80px 1fr;
	align-items: center;
	gap: 8px;
}

.pfb-insp-row--col {
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
	padding: 5px 8px;
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

.pfb-type-badge {
	font-size: 10px;
	color: var(--text-muted);
	background: var(--gray-100);
	border: 1px solid var(--gray-300);
	border-radius: var(--border-radius-sm);
	padding: 1px 5px;
	white-space: nowrap;
	flex-shrink: 0;
}

/* ── Input ───────────────────────────────────────────────── */
.pfb-insp-input {
	width: 100%;
	padding: 6px 8px;
	font-size: var(--text-sm);
	border: 1px solid var(--border-color);
	border-radius: var(--border-radius);
	background: var(--fg-color);
	color: var(--text-color);
	outline: none;
	box-sizing: border-box;
}

.pfb-insp-input:focus {
	border-color: var(--gray-500);
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
	padding: 5px 6px;
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

/* ── Hint / placeholder ──────────────────────────────────── */
.pfb-insp-hint {
	font-size: var(--text-sm);
	line-height: 1.5;
}

.pfb-insp-placeholder {
	align-items: center;
	justify-content: center;
	padding: 24px;
	text-align: center;
}

/* ── Actions ─────────────────────────────────────────────── */
.pfb-insp-actions {
	padding: 12px 14px;
	margin-top: auto;
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
	padding: 5px 10px;
	font-size: var(--text-sm);
	cursor: pointer;
}

.btn-danger-subtle:hover {
	background: var(--red-50);
	border-color: var(--red-300);
}
</style>
