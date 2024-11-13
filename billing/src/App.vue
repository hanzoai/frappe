<template>
	<div class="flex h-screen w-screen">
		<div class="h-full border-r bg-gray-50">
			<AppSidebar />
		</div>
		<div class="flex-1 flex flex-col h-full overflow-auto px-28">
			<router-view />
		</div>
	</div>
	<Dialogs />
	<Toasts />
</template>

<script setup>
import AppSidebar from '@/components/AppSidebar.vue'
import { Dialogs } from '@/dialogs.js'
import { Toasts } from 'frappe-ui'
</script>
