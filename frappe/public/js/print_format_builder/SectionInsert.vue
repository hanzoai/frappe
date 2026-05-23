<template>
	<div class="section-insert" @click="$emit('insert')">
		<div class="section-insert-line"></div>
		<button class="section-insert-btn" :title="__('Add section here')">
			<svg class="icon icon-xs"><use href="#icon-plus"></use></svg>
		</button>
		<div class="section-insert-line"></div>
	</div>
</template>

<script setup>
defineEmits(["insert"]);
</script>

<style scoped>
.section-insert {
	display: flex;
	align-items: center;
	height: 1.25rem;
	cursor: pointer;
	opacity: 0;
	transition: opacity 0.15s ease;
}

.section-insert:hover {
	opacity: 1;
}

.section-insert-line {
	flex: 1;
	height: 1.5px;
	background: var(--primary);
	border-radius: 1px;
}

.section-insert-btn {
	flex-shrink: 0;
	width: 18px;
	height: 18px;
	border-radius: 50%;
	border: 1.5px solid var(--primary);
	background: white;
	color: var(--primary);
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 0;
	margin: 0 4px;
	cursor: pointer;
	box-shadow: none;
}

.section-insert-btn:hover {
	background: var(--primary);
	color: white;
}
</style>
