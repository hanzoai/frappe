<template>
	<div class="file-web-link margin-bottom">
<<<<<<< HEAD
		<a href class="text-muted text-medium" @click.prevent="emit('hide-web-link')">
=======
		<a href class="text-muted text-medium" @click.prevent="$emit('hide-web-link')">
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			{{ __("← Back to upload files") }}
		</a>
		<div class="input-group">
			<input
				type="text"
				class="form-control"
				:placeholder="__('Attach a web link')"
				v-model="url"
			/>
		</div>
	</div>
</template>
<<<<<<< HEAD

<script setup>
import { ref } from "vue";

// emits
let emit = defineEmits(["hide-web-link"]);

let url = ref("");

defineExpose({ url });
</script>

<style scoped>
=======
<script>
export default {
	name: "WebLink",
	data() {
		return {
			url: "",
		};
	},
};
</script>

<style>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
.file-web-link .input-group {
	margin-top: 10px;
}
</style>
