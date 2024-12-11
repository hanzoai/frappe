<template>
	<div class="layout-main-section row" v-if="shouldRender">
		<div class="col-3">
			<PrintFormatControls />
		</div>
		<div class="print-format-container col-9">
<<<<<<< HEAD
			<KeepAlive>
				<component :is="Preview" v-if="show_preview" />
				<component :is="PrintFormat" v-else />
			</KeepAlive>
=======
			<keep-alive>
				<Preview v-if="show_preview" />
				<PrintFormat v-else />
			</keep-alive>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		</div>
	</div>
</template>

<<<<<<< HEAD
<script setup>
=======
<script>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
import PrintFormat from "./PrintFormat.vue";
import Preview from "./Preview.vue";
import PrintFormatControls from "./PrintFormatControls.vue";
import { getStore } from "./store";
<<<<<<< HEAD
import { computed, ref, onMounted, provide } from "vue";

// props
const props = defineProps(["print_format_name"]);

// variables
let show_preview = ref(false);

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

// mounted
onMounted(() => {
	$store.value.fetch().then(() => {
		if (!$store.value.layout.value) {
			$store.value.layout.value = $store.value.get_default_layout();
			$store.value.save_changes();
		}
	});
});

defineExpose({ toggle_preview, $store });
=======

export default {
	name: "PrintFormatBuilder",
	props: ["print_format_name"],
	components: {
		PrintFormat,
		PrintFormatControls,
		Preview,
	},
	data() {
		return {
			show_preview: false,
		};
	},
	provide() {
		return {
			$store: this.$store,
		};
	},
	mounted() {
		this.$store.fetch().then(() => {
			if (!this.$store.layout) {
				this.$store.layout = this.$store.get_default_layout();
				this.$store.save_changes();
			}
		});
	},
	methods: {
		toggle_preview() {
			this.show_preview = !this.show_preview;
		},
	},
	computed: {
		$store() {
			return getStore(this.print_format_name);
		},
		shouldRender() {
			return Boolean(this.$store.print_format && this.$store.meta && this.$store.layout);
		},
	},
};
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
</script>

<style scoped>
.print-format-container {
	height: calc(100vh - 140px);
	overflow-y: auto;
	padding-top: 0.5rem;
	padding-bottom: 4rem;
}
</style>
