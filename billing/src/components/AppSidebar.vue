<template>
	<div
		class="relative flex h-full flex-col justify-between transition-all duration-300 ease-in-out"
		:class="isSidebarCollapsed ? 'w-12' : 'w-[220px]'"
	>
		<div class="flex-1 mt-3 overflow-y-auto">
			<div class="mb-3 flex flex-col">
				<SidebarLink
					:label="previousRoute ? 'Back to app' : 'Back'"
					icon="chevron-left"
					:isCollapsed="isSidebarCollapsed"
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
					:isCollapsed="isSidebarCollapsed"
					class="mx-2 my-0.5"
				/>
			</nav>
		</div>
		<div class="m-2 flex flex-col gap-1">
			<SidebarLink
				:label="isSidebarCollapsed ? 'Expand' : 'Collapse'"
				:isCollapsed="isSidebarCollapsed"
				@click="isSidebarCollapsed = !isSidebarCollapsed"
			>
				<template #icon>
					<span class="grid h-4.5 w-4.5 flex-shrink-0 place-items-center">
						<CollapseSidebarIcon
							class="h-4.5 w-4.5 text-gray-700 duration-300 ease-in-out"
							:class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }"
						/>
					</span>
				</template>
			</SidebarLink>
		</div>
	</div>
</template>
<script setup>
import CollapseSidebarIcon from '@/icons/CollapseSidebarIcon.vue'
import BillingIcon from '@/icons/BillingIcon.vue'
import Plans from '@/icons/PlansIcon.vue'
import InvoiceIcon from '@/icons/InvoiceIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import Generic from '@/logo/Generic.vue'
import { FeatherIcon } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { onMounted } from 'vue'

const router = useRouter()
const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)
const previousRoute = useStorage('previousRoute', null)

onMounted(() => {
	if (document.referrer) {
		previousRoute.value = document.referrer
	}
})

const links = [
	{
		label: 'Billing',
		icon: BillingIcon,
		to: 'Billing',
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
		icon: Generic,
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
