<template>
	<div v-if="is_shown" class="flex justify-between build-success-message align-center">
		Compiled successfully
		<a v-if="!live_reload" class="ml-4 text-white underline" href="/" @click.prevent="reload">
			Refresh
		</a>
	</div>
</template>
<<<<<<< HEAD

<script setup>
import { ref } from "vue";

// variables
let is_shown = ref(false);
let live_reload = ref(false);
let timeout = ref(null);

// Methods
function show(data) {
	if (data.live_reload) {
		live_reload.value = true;
		reload();
	}

	is_shown.value = true;
	if (timeout.value) {
		clearTimeout(timeout.value);
	}
	timeout.value = setTimeout(() => {
		hide();
	}, 10000);
}
function hide() {
	is_shown.value = false;
}
function reload() {
	window.location.reload();
}

defineExpose({ show, hide });
</script>

<style scoped>
=======
<script>
export default {
	name: "BuildSuccess",
	data() {
		return {
			is_shown: false,
			live_reload: false,
		};
	},
	methods: {
		show(data) {
			if (data.live_reload) {
				this.live_reload = true;
				this.reload();
			}

			this.is_shown = true;
			if (this.timeout) {
				clearTimeout(this.timeout);
			}
			this.timeout = setTimeout(() => {
				this.hide();
			}, 10000);
		},
		hide() {
			this.is_shown = false;
		},
		reload() {
			window.location.reload();
		},
	},
};
</script>
<style>
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
.build-success-message {
	position: fixed;
	z-index: 9999;
	bottom: 0;
	right: 0;
	background: rgba(0, 0, 0, 0.6);
	border-radius: var(--border-radius);
	padding: 0.5rem 1rem;
	color: white;
	font-weight: 500;
	margin: 1rem;
}
</style>
