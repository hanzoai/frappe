<template>
	<div v-if="isFCSite.data" class="flex h-screen w-screen">
		<div class="h-full border-r bg-gray-50">
			<AppSidebar />
		</div>
		<div class="flex-1 flex flex-col h-full overflow-auto px-28">
			<router-view />
		</div>
		<Dialogs />
		<Toasts />
	</div>
	<PageNotFound v-else />
</template>

<script setup>
import PageNotFound from './pages/PageNotFound.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import { Dialogs } from '@/dialogs.js'
import { Toasts, createResource } from 'frappe-ui'

const isFCSite = createResource({
	url: 'frappe.integrations.frappe_providers.frappecloud_billing.is_fc_site',
	cache: 'isFCSite',
	auto: true,
	transform: (data) => Boolean(data),
})
</script>
