<template>
	<div class="print-format-section-container" v-if="!section.remove">
		<div class="print-format-section">
			<div class="section-toolbar">
				<div class="section-toolbar-left">
					<div class="drag-handle section-drag-handle" title="Drag to reorder">
						<svg class="icon icon-sm"><use href="#icon-drag"></use></svg>
					</div>
					<input
						class="input-section-label"
						type="text"
						:placeholder="__('Section Title')"
						v-model="section.label"
					/>
					<span
						v-if="section.field_orientation == 'left-right'"
						class="orientation-badge"
						:title="__('Labels left, values right')"
					>
						L→V
					</span>
				</div>
				<div class="section-toolbar-right">
					<div class="column-layout-buttons" :title="__('Number of columns')">
						<button
							v-for="n in [1, 2, 3, 4]"
							:key="n"
							class="btn btn-xs column-btn"
							:class="{ active: section.columns.length === n }"
							@click.stop="set_columns(n)"
						>
							{{ n }}
						</button>
					</div>
					<button
						class="btn btn-xs btn-icon toolbar-btn"
						:class="{ active: section.field_orientation == 'left-right' }"
						:title="__('Toggle label orientation (Left→Right)')"
						@click.stop="toggle_orientation"
					>
						<svg class="icon icon-sm"><use href="#icon-align-justify"></use></svg>
					</button>
					<button
						class="btn btn-xs btn-icon toolbar-btn"
						:class="{ active: section.page_break }"
						:title="
							section.page_break ? __('Remove page break') : __('Add page break')
						"
						@click.stop="toggle_page_break"
					>
						<svg class="icon icon-sm"><use href="#icon-separator-vertical"></use></svg>
					</button>
					<button
						class="btn btn-xs btn-icon toolbar-btn toolbar-btn-danger"
						:title="__('Remove section')"
						@click.stop="section['remove'] = true"
					>
						<svg class="icon icon-sm"><use href="#icon-x"></use></svg>
					</button>
				</div>
			</div>

			<div class="section-columns">
				<template v-for="(column, i) in section.columns" :key="i">
					<div class="column-divider" v-if="i > 0"></div>
					<div class="column">
						<draggable
							class="drag-container"
							v-model="column.fields"
							group="fields"
							:animation="150"
							item-key="id"
							handle=".drag-handle"
						>
							<template #item="{ element }">
								<Field :df="element" />
							</template>
							<template #footer>
								<div
									v-if="column.fields.filter((f) => !f.remove).length === 0"
									class="empty-drop-zone"
								>
									<button
										v-if="section.columns.length > 1"
										class="btn btn-xs btn-icon empty-col-remove"
										:title="__('Remove column')"
										@click.stop="remove_column(i)"
									>
										<svg class="icon icon-xs">
											<use href="#icon-x"></use>
										</svg>
									</button>
									<svg class="icon icon-sm text-muted">
										<use href="#icon-plus"></use>
									</svg>
									<span class="text-muted">{{ __("Drop fields here") }}</span>
								</div>
							</template>
						</draggable>
					</div>
				</template>
			</div>
		</div>
		<div class="page-break-indicator" v-if="section.page_break">
			<span>— {{ __("Page Break") }} —</span>
		</div>
	</div>
</template>

<script setup>
import draggable from "vuedraggable";
import Field from "./Field.vue";

const props = defineProps(["section"]);

function set_columns(n) {
	const current = props.section.columns.length;
	if (n === current) return;

	// collect all fields preserving order
	const all_fields = props.section.columns.flatMap((col) => col.fields);

	// build n fresh columns and distribute fields round-robin
	const new_columns = Array.from({ length: n }, () => ({ label: "", fields: [] }));
	all_fields.forEach((field, i) => new_columns[i % n].fields.push(field));

	props.section.columns = new_columns;
}

function remove_column(index) {
	if (props.section.columns.length <= 1) return;
	props.section.columns.splice(index, 1);
}

function toggle_page_break() {
	props.section["page_break"] = !props.section.page_break;
}

function toggle_orientation() {
	props.section["field_orientation"] =
		props.section.field_orientation === "left-right" ? "" : "left-right";
}
</script>

<style scoped>
.print-format-section-container {
	position: relative;
}

.print-format-section-container:not(:last-child) {
	margin-bottom: 0.5rem;
}

.print-format-section {
	background-color: white;
	border: 1px solid var(--dark-border-color);
	border-radius: var(--border-radius);
	overflow: hidden;
}

.section-toolbar {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0.4rem 0.6rem;
	background: var(--gray-50);
	border-bottom: 1px solid var(--border-color);
	gap: 0.5rem;
}

.section-toolbar-left {
	display: flex;
	align-items: center;
	gap: 0.4rem;
	flex: 1;
	min-width: 0;
}

.section-toolbar-right {
	display: flex;
	align-items: center;
	gap: 0.25rem;
	flex-shrink: 0;
}

.section-drag-handle {
	cursor: grab;
	color: var(--gray-400);
	display: flex;
	align-items: center;
	padding: 2px;
}

.section-drag-handle:hover {
	color: var(--gray-600);
}

.input-section-label {
	border: 1px solid transparent;
	border-radius: var(--border-radius);
	font-size: var(--text-sm);
	font-weight: 600;
	background: transparent;
	padding: 2px 4px;
	flex: 1;
	min-width: 0;
}

.input-section-label:hover {
	border-color: var(--border-color);
}

.input-section-label:focus {
	border-color: var(--primary);
	outline: none;
	background-color: white;
}

.input-section-label::placeholder {
	font-style: italic;
	font-weight: normal;
	color: var(--gray-400);
}

.orientation-badge {
	font-size: 10px;
	color: var(--text-muted);
	background: var(--gray-100);
	border: 1px solid var(--border-color);
	border-radius: var(--border-radius-sm);
	padding: 1px 4px;
	white-space: nowrap;
}

.column-layout-buttons {
	display: flex;
	background: var(--gray-100);
	border: 1px solid var(--border-color);
	border-radius: var(--border-radius);
	overflow: hidden;
}

.column-btn {
	padding: 2px 6px;
	font-size: 11px;
	font-weight: 500;
	border: none;
	border-radius: 0;
	background: transparent;
	box-shadow: none;
	color: var(--text-muted);
	min-width: 20px;
}

.column-btn:not(:first-child) {
	border-left: 1px solid var(--border-color);
}

.column-btn:hover {
	background: var(--gray-200);
	color: var(--text-color);
}

.column-btn.active {
	background: var(--primary);
	color: white;
}

.toolbar-btn {
	padding: 3px;
	box-shadow: none;
	color: var(--text-muted);
	border-radius: var(--border-radius-sm);
}

.toolbar-btn:hover {
	background: var(--gray-200);
	color: var(--text-color);
}

.toolbar-btn.active {
	background: var(--blue-50);
	color: var(--blue-500);
}

.toolbar-btn-danger:hover {
	background: var(--red-50);
	color: var(--red-500);
}

.section-columns {
	display: flex;
	padding: 0.75rem;
	gap: 0;
	align-items: stretch;
}

.column {
	flex: 1;
	min-width: 0;
	display: flex;
}

.column-divider {
	width: 1px;
	background: var(--border-color);
	margin: 0 0.5rem;
	flex-shrink: 0;
}

.drag-container {
	flex: 1;
	min-width: 0;
	min-height: 2.5rem;
	border-radius: var(--border-radius);
	display: flex;
	flex-direction: column;
	gap: 0.4rem;
	overflow: hidden;
}

.empty-drop-zone {
	position: relative;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.25rem;
	min-height: 3rem;
	border: 1.5px dashed var(--gray-300);
	border-radius: var(--border-radius);
	color: var(--text-muted);
	font-size: var(--text-xs);
}

.empty-col-remove {
	position: absolute;
	top: 4px;
	right: 4px;
	padding: 2px;
	box-shadow: none;
	color: var(--gray-500);
	opacity: 0;
	transition: opacity 0.1s;
}

.empty-drop-zone:hover .empty-col-remove {
	opacity: 1;
}

.empty-col-remove:hover {
	background: var(--red-50);
	color: var(--red-500);
}

.page-break-indicator {
	text-align: center;
	color: var(--text-muted);
	font-size: var(--text-xs);
	font-style: italic;
	padding: 0.25rem 0;
	border-top: 1px dashed var(--gray-300);
	border-bottom: 1px dashed var(--gray-300);
	margin: 0.25rem 0;
}
</style>
