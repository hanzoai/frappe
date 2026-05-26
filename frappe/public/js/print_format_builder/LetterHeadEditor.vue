<template>
	<div
		class="letterhead"
		:class="{ 'letterhead--selected': store.selected_letterhead.value }"
		@click.stop="select_letterhead"
	>
		<div v-if="letterhead" v-html="letterhead.content"></div>
		<div v-else class="letterhead-empty">
			<span v-html="frappe.utils.icon('image', 'sm')"></span>
			<span>{{ __("No Letter Head — click to add") }}</span>
		</div>
	</div>
</template>

<script setup>
import { useStore } from "./store";
import { get_image_dimensions } from "./utils";
import { ref, watch, onMounted, inject } from "vue";

let { letterhead, store, layout } = useStore();
let raw_store = inject("$store");

let aspect_ratio = ref(null);
let range_input_field = ref(null);

function select_letterhead() {
	raw_store.selected_letterhead.value = true;
	raw_store.selected_field.value = null;
	raw_store.selected_section.value = null;
}

function set_letterhead(_letterhead) {
	store.value.change_letterhead(_letterhead);
}

onMounted(() => {
	if (!letterhead.value && !layout.value?.letter_head) {
		const lh_name = frappe.boot.sysdefaults.letter_head;
		if (lh_name) set_letterhead(lh_name);
	}
});

// Maintain aspect ratio when slider moves
watch(
	() => (letterhead.value ? letterhead.value[range_input_field.value] : null),
	() => {
		if (aspect_ratio.value === null) return;
		let update_field =
			range_input_field.value == "image_width" ? "image_height" : "image_width";
		letterhead.value[update_field] =
			update_field == "image_width"
				? aspect_ratio.value * letterhead.value.image_height
				: letterhead.value.image_width / aspect_ratio.value;
	}
);

// Initialize slider state when letterhead image is set/replaced
watch(
	letterhead,
	(lh) => {
		if (lh?.image) {
			get_image_dimensions(lh.image).then(({ width, height }) => {
				aspect_ratio.value = width / height;
				range_input_field.value = aspect_ratio.value > 1 ? "image_width" : "image_height";
			});
		}
	},
	{ immediate: true }
);

// Rebuild content HTML whenever image dimensions or alignment change
watch(
	letterhead,
	() => {
		if (!letterhead.value) return;
		if (letterhead.value.image_width && letterhead.value.image_height) {
			let dimension =
				letterhead.value.image_width > letterhead.value.image_height ? "width" : "height";
			let dimension_value = letterhead.value["image_" + dimension];
			letterhead.value.content = `
			<div style="text-align: ${letterhead.value.align.toLowerCase()};">
				<img
					src="${letterhead.value.image}"
					alt="${letterhead.value.name}"
					${dimension}="${dimension_value}"
					style="${dimension}: ${dimension_value}px;">
			</div>
		`;
		}
	},
	{ deep: true },
	{ immediate: true }
);

// Expose for inspector
defineExpose({ aspect_ratio, range_input_field });
</script>

<style scoped>
.letterhead {
	position: relative;
	border: 1px solid transparent;
	border-radius: var(--border-radius);
	padding: 1rem;
	margin-bottom: 1rem;
	cursor: pointer;
	transition: border-color 0.15s, box-shadow 0.15s;
}

.letterhead:hover {
	border-color: var(--gray-300);
}

.letterhead--selected {
	border-color: var(--primary);
	box-shadow: 0 0 0 2px var(--primary-light);
}

.letterhead-empty {
	display: flex;
	align-items: center;
	gap: 6px;
	color: var(--text-muted);
	font-size: var(--text-sm);
	padding: 0.5rem 0;
}
</style>
