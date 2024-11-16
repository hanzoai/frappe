<template>
	<div
		class="relative flex h-full flex-col justify-between transition-all duration-300 ease-in-out w-[220px]"
	>
		<div>
			<UserDropdown class="p-2" />
		</div>
		<div class="flex-1 overflow-y-auto">
			<div class="mb-3 flex flex-col">
				<SidebarLink
					:label="previousRoute ? 'Back to app' : 'Back'"
					icon="arrow-left"
					@click="goBack"
					class="relative mx-2 my-0.5"
				/>
			</div>
			<nav class="mb-3 flex flex-col">
				<SidebarLink
					v-for="link in links"
					:icon="link.icon"
					:label="link.label"
					:to="link.to"
					class="mx-2 my-0.5"
				/>
			</nav>
		</div>
		<div class="m-2 text-base text-gray-600 p-2 flex justify-center">
			Powered by Frappe Cloud
		</div>
	</div>
</template>
<script setup>
import UserDropdown from '@/components/UserDropdown.vue'
import BillingIcon from '@/icons/BillingIcon.vue'
import CardIcon from '@/icons/CardIcon.vue'
import Plans from '@/icons/PlansIcon.vue'
import InvoiceIcon from '@/icons/InvoiceIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { onMounted } from 'vue'

const router = useRouter()
const previousRoute = useStorage('previousRoute', null)

onMounted(() => {
	if (document.referrer) {
		previousRoute.value = document.referrer
	}
})

const links = [
	{
		label: 'Overview',
		icon: BillingIcon,
		to: 'Overview',
	},
	{
		label: 'Plans',
		icon: Plans,
		to: 'Plans',
	},
	{
		label: 'Invoices',
		icon: InvoiceIcon,
		to: 'Invoices',
	},
	{
		label: 'Cards',
		icon: CardIcon,
		to: 'Cards',
	},
]

function goBack() {
	if (previousRoute.value) {
		window.location.href = previousRoute.value
	} else {
		router.go(-1)
	}
}
</script>
