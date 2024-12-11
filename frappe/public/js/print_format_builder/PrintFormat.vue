<template>
	<div class="print-format-main" :style="rootStyles">
		<div :style="page_number_style">{{ __("1 of 2") }}</div>

		<LetterHeadEditor type="Header" />
		<HTMLEditor
			:value="layout.header"
<<<<<<< HEAD
			@change="layout.header = $event"
=======
			@change="$set(layout, 'header', $event)"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			:button-label="__('Edit Header')"
		/>
		<draggable
			class="mb-4"
			v-model="layout.sections"
			group="sections"
			filter=".section-columns, .column, .field"
			:animation="200"
<<<<<<< HEAD
			item-key="id"
		>
			<template #item="{ element }">
				<PrintFormatSection
					:section="element"
					@add_section_above="add_section_above(element)"
				/>
			</template>
		</draggable>
		<HTMLEditor
			:value="layout.footer"
			@change="layout.footer = $event"
=======
		>
			<PrintFormatSection
				v-for="(section, i) in layout.sections"
				:key="i"
				:section="section"
				@add_section_above="add_section_above(section)"
			/>
		</draggable>
		<HTMLEditor
			:value="layout.footer"
			@change="$set(layout, 'footer', $event)"
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			:button-label="__('Edit Footer')"
		/>
		<HTMLEditor
			v-if="letterhead"
			:value="letterhead.footer"
			@change="update_letterhead_footer"
			:button-label="__('Edit Letter Head Footer')"
		/>
	</div>
</template>

<<<<<<< HEAD
<script setup>
=======
<script>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
import draggable from "vuedraggable";
import HTMLEditor from "./HTMLEditor.vue";
import LetterHeadEditor from "./LetterHeadEditor.vue";
import PrintFormatSection from "./PrintFormatSection.vue";
<<<<<<< HEAD
import { useStore } from "./store";
import { computed, inject, watch } from "vue";

// mixins
let { layout, letterhead, print_format } = useStore();
let store = inject("$store");
// methods
function add_section_above(section) {
	let sections = [];
	for (let _section of layout.value.sections) {
		if (_section === section) {
			sections.push({
				label: "",
				columns: [
					{ label: "", fields: [] },
					{ label: "", fields: [] },
				],
			});
		}
		sections.push(_section);
	}
	layout.value["sections"] = sections;
}
function update_letterhead_footer(val) {
	letterhead.value.footer = val;
}

// computed
let rootStyles = computed(() => {
	let {
		margin_top = 0,
		margin_bottom = 0,
		margin_left = 0,
		margin_right = 0,
	} = print_format.value;
	return {
		padding: `${margin_top}mm ${margin_right}mm ${margin_bottom}mm ${margin_left}mm`,
		width: "210mm",
		minHeight: "297mm",
	};
});
let page_number_style = computed(() => {
	let style = {
		position: "absolute",
		background: "white",
		padding: "4px",
		borderRadius: "var(--border-radius)",
		border: "1px solid var(--border-color)",
	};
	if (print_format.value.page_number.includes("Top")) {
		style.top = print_format.value.margin_top / 2 + "mm";
		style.transform = "translateY(-50%)";
	}
	if (print_format.value.page_number.includes("Left")) {
		style.left = print_format.value.margin_left + "mm";
	}
	if (print_format.value.page_number.includes("Right")) {
		style.right = print_format.value.margin_right + "mm";
	}
	if (print_format.value.page_number.includes("Bottom")) {
		style.bottom = print_format.value.margin_bottom / 2 + "mm";
		style.transform = "translateY(50%)";
	}
	if (print_format.value.page_number.includes("Center")) {
		style.left = "50%";
		style.transform += " translateX(-50%)";
	}
	if (print_format.value.page_number.includes("Hide")) {
		style.display = "none";
	}

	return style;
});

watch(layout, () => (store.dirty.value = true), { deep: true });
watch(print_format, () => (store.dirty.value = true), { deep: true });
=======
import { storeMixin } from "./store";

export default {
	name: "PrintFormat",
	mixins: [storeMixin],
	components: {
		draggable,
		PrintFormatSection,
		LetterHeadEditor,
		HTMLEditor,
	},
	computed: {
		rootStyles() {
			let {
				margin_top = 0,
				margin_bottom = 0,
				margin_left = 0,
				margin_right = 0,
			} = this.print_format;
			return {
				padding: `${margin_top}mm ${margin_right}mm ${margin_bottom}mm ${margin_left}mm`,
				width: "210mm",
				minHeight: "297mm",
			};
		},
		page_number_style() {
			let style = {
				position: "absolute",
				background: "white",
				padding: "4px",
				borderRadius: "var(--border-radius)",
				border: "1px solid var(--border-color)",
			};
			if (this.print_format.page_number.includes("Top")) {
				style.top = this.print_format.margin_top / 2 + "mm";
				style.transform = "translateY(-50%)";
			}
			if (this.print_format.page_number.includes("Left")) {
				style.left = this.print_format.margin_left + "mm";
			}
			if (this.print_format.page_number.includes("Right")) {
				style.right = this.print_format.margin_right + "mm";
			}
			if (this.print_format.page_number.includes("Bottom")) {
				style.bottom = this.print_format.margin_bottom / 2 + "mm";
				style.transform = "translateY(50%)";
			}
			if (this.print_format.page_number.includes("Center")) {
				style.left = "50%";
				style.transform += " translateX(-50%)";
			}
			if (this.print_format.page_number.includes("Hide")) {
				style.display = "none";
			}

			return style;
		},
	},
	methods: {
		add_section_above(section) {
			let sections = [];
			for (let _section of this.layout.sections) {
				if (_section === section) {
					sections.push({
						label: "",
						columns: [
							{ label: "", fields: [] },
							{ label: "", fields: [] },
						],
					});
				}
				sections.push(_section);
			}
			this.$set(this.layout, "sections", sections);
		},
		update_letterhead_footer(val) {
			this.letterhead.footer = val;
			this.letterhead._dirty = true;
		},
	},
};
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
</script>

<style scoped>
.print-format-main {
	position: relative;
	margin-right: auto;
	margin-left: auto;
	background-color: white;
	box-shadow: var(--shadow-lg);
	border-radius: var(--border-radius);
}
</style>
