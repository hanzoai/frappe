<script setup>
import { ref, computed } from "vue";

const props = defineProps({
	modelValue: {
		type: Boolean,
		default: true,
	},
	title: {
		type: String,
		default: "Welcome",
	},
	steps: {
		type: Array,
		default: () => [],
	},
	minimizeIcon: {
		type: String,
		default: "—",
	},
	closeIcon: {
		type: String,
		default: "✕",
	},
	headerIcon: {
		type: String,
		default: "👋",
	},
	checklistIcon: {
		type: String,
		default: "✔",
	},
	completeChecklistIcon: {
		type: String,
		default: "✔",
	},
});

const emit = defineEmits(["update:modelValue", "skip"]);

const collapsed = ref(false);

const visible = computed({
	get: () => props.modelValue,
	set: (val) => emit("update:modelValue", val),
});

const completedCount = computed(
	() => props.steps.filter((step) => step.is_complete || step.is_skipped).length
);

const progress = computed(() => {
	if (!props.steps.length) return 0;
	return Math.round((completedCount.value / props.steps.length) * 100);
});

function close() {
	visible.value = false;
}

function toggleCollapse() {
	collapsed.value = !collapsed.value;
}

function skipAll(skips) {
	skips.forEach((step) => {
		if (!step.is_complete && !step.is_skipped) {
			markSkip(step);
		}
	});
}

function handleAction(step) {
	if (step.is_complete) return;

	const actions = {
		"Create Entry": createEntry,
		"Show Form Tour": showFormTour,
		"Update Settings": updateSettings,
		"View Report": openReport,
		"Go to Page": goToPage,
	};

	if (step.action && actions[step.action]) {
		actions[step.action](step);
	} else if (step.route) {
		frappe.set_route(step.route);
	}
}

function goToPage(step) {
	frappe.set_route(step.path).then(() => {
		markComplete(step);
	});
}

function openReport(step) {
	const route = frappe.utils.generate_route({
		name: step.reference_report,
		type: "report",
		is_query_report: step.report_type !== "Report Builder",
		doctype: step.report_reference_doctype,
	});

	frappe.set_route(route).then(() => {
		markComplete(step);
	});
}

function showFormTour(step) {
	let route = step.is_single
		? frappe.router.slug(step.reference_document)
		: `${frappe.router.slug(step.reference_document)}/new`;

	frappe.route_hooks = {};
	frappe.route_hooks.after_load = (frm) => {
		const tour_name = step.form_tour;
		on_finish = () => markComplete(step);

		frm.tour
			.init({ tour_name, on_finish: () => markComplete(step) })
			.then(() => frm.tour.start());
	};

	frappe.set_route(route);
}

function updateSettings(step) {
	frappe.route_hooks = {};
	frappe.route_hooks.after_load = (frm) => {
		frm.scroll_to_field(step.field);
		frm.doc.__unsaved = true;
	};

	frappe.route_hooks.after_save = (frm) => {
		const success = frm.doc[step.field] == step.value_to_validate;

		if (success) {
			markComplete(step);
		}
	};

	frappe.set_route("Form", step.reference_document);
}

async function createEntry(step) {
	toggleCollapse();

	frappe.route_hooks = {};
	frappe.route_hooks.after_load = (frm) => {
		const tour_name = step.form_tour;
		if (tour_name) {
			on_finish = () => {
				console.log("Tour finished");
			};
			frm.tour.init({ tour_name, on_finish }).then(() => frm.tour.start());
		}
	};

	const callback = () => {
		markComplete(step);
	};

	frappe.route_hooks.after_save = callback;

	if (step.show_full_form) {
		frappe.set_route("Form", step.reference_document, "new");
	} else {
		frappe.new_doc(step.reference_document);
	}
}

function markComplete(step) {
	step.is_complete = true;

	frappe.call("frappe.desk.desktop.update_onboarding_step", {
		name: step.name,
		field: "is_complete",
		value: 1,
	});
}

function markSkip(step) {
	step.is_skipped = true;

	frappe.call("frappe.desk.desktop.update_onboarding_step", {
		name: step.name,
		field: "is_skipped",
		value: 1,
	});
}

function markReset(step) {
	step.is_skipped = false;

	frappe.call("frappe.desk.desktop.update_onboarding_step", {
		name: step.name,
		field: "is_skipped",
		value: 0,
	});
}
</script>

<template>
	<div v-if="visible" class="onb-panel">
		<!-- Header -->
		<div class="header onb-header-main">
			<div class="onb-header-left">
				<div class="onb-header-logo" v-html="headerIcon"></div>
				<h4 class="onb-header-title">{{ title }}</h4>
			</div>

			<div class="onb-header-actions">
				<button @click="toggleCollapse" v-html="minimizeIcon"></button>
				<button @click="close" v-html="closeIcon"></button>
			</div>
		</div>

		<!-- Body -->
		<div v-if="!collapsed" class="body">
			<div class="intro">
				<p>{{ completedCount }}/{{ steps.length }} steps completed</p>
			</div>

			<div class="onb-progress">
				<div class="onboarding-progress-bar" :style="{ width: progress + '%' }"></div>
			</div>

			<div class="onb-progress-label">
				{{ progress }}% completed
				<span class="onb-skip" @click="skipAll(steps)">Skip all</span>
			</div>

			<!-- Steps -->
			<div class="onb-steps flex flex-col gap-2.5 overflow-hidden">
				<div
					style="width: 100%"
					v-for="(step, i) in steps"
					:key="i"
					:class="{ is_complete: step.is_complete }"
				>
					<div
						class="onb-group w-full step-title flex items-center"
						style="align-items: center"
						:class="
							step.is_complete
								? 'text-extra-muted onb-cursor-disabled'
								: 'text-ink-gray-8 onb-select-cursor'
						"
					>
						<div class="onb-step-left">
							<div class="onb-step-icon" v-if="step.is_complete">
								<div v-html="completeChecklistIcon"></div>
							</div>
							<div class="onb-step-icon" v-else>
								<div v-html="checklistIcon"></div>
							</div>

							<div v-if="!step.is_skipped">
								<span class="text-base onb-step-text" @click="handleAction(step)">
									{{ step.action_label }}
								</span>
							</div>
							<div v-else>
								<span
									class="text-base onb-step-text"
									style="text-decoration-line: line-through"
								>
									{{ step.action_label }}
								</span>
							</div>
						</div>

						<div v-if="!step.is_complete">
							<div v-if="!step.is_skipped">
								<div
									class="ml-auto text-base onb-show-on-hover text-sm w-12 text-right text-ink-gray-8"
								>
									<span
										style="
											font-size: 12px;
											vertical-align: text-top;
											margin-right: 10px;
										"
										@click="markSkip(step)"
									>
										{{ __("Skip") }}
									</span>
								</div>
							</div>
							<div v-if="step.is_skipped">
								<div
									class="ml-auto text-base onb-show-on-hover text-sm w-12 text-right text-ink-gray-8"
								>
									<span
										style="
											font-size: 12px;
											vertical-align: text-top;
											margin-right: 10px;
										"
										@click="markReset(step)"
									>
										{{ __("Reset") }}
									</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
