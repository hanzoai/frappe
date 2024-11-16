<template>
	<div class="flex h-full flex-col overflow-hidden">
		<h2 class="flex items-center h-7 text-xl font-semibold leading-5 px-60 my-8">
			{{ 'Overview' }}
		</h2>
		<div v-if="team.data" class="px-60 overflow-y-auto">
			<CurrentPlan @changePlan="router.push({ name: 'Plans' })" />
			<div class="bg-gray-100 h-px my-7" />
			<PaymentDetails />
		</div>
		<div v-else class="flex flex-1 items-center justify-center">
			<Spinner class="size-8" />
		</div>
	</div>
</template>
<script setup>
import CurrentPlan from '@/components/CurrentPlan.vue'
import PaymentDetails from '@/components/PaymentDetails.vue'
import { Spinner, createResource } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { computed, provide, inject } from 'vue'

const router = useRouter()

const team = inject('team')

const upcomingInvoice = createResource({
	url: 'frappe.integrations.frappe_providers.frappecloud_billing.api',
	params: { method: 'billing.upcoming_invoice' },
	cache: 'upcomingInvoice',
	auto: true,
})

provide('billing', {
	availableCredits: computed(() => upcomingInvoice.data?.available_credits),
	currentBillingAmount: computed(() => upcomingInvoice.data?.upcoming_invoice.total),
	reloadUpcomingInvoice: upcomingInvoice.reload,
})
</script>
