<template>
	<div class="flex h-full flex-col py-11 px-[68px] gap-8 overflow-y-auto">
		<h2 class="flex gap-2 text-xl font-semibold leading-5">
			{{ 'Billing' }}
		</h2>
		<div v-if="team.data">
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
import { computed, provide } from 'vue'

const router = useRouter()

const team = createResource({
	url: 'frappe.integrations.frappe_providers.frappecloud_billing.api',
	params: { method: 'team.info' },
	cache: 'team',
	auto: true,
})

const upcomingInvoice = createResource({
	url: 'frappe.integrations.frappe_providers.frappecloud_billing.api',
	params: { method: 'billing.upcoming_invoice' },
	cache: 'upcomingInvoice',
	auto: true,
})

provide('billing', {
	team: computed(() => team.data),
	reloadTeam: team.reload,
	availableCredits: computed(() => upcomingInvoice.data?.available_credits),
	currentBillingAmount: computed(() => upcomingInvoice.data?.upcoming_invoice.total),
	reloadUpcomingInvoice: upcomingInvoice.reload,
})
</script>
