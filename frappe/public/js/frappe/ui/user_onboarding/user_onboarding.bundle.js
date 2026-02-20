import { createApp, ref, h } from "vue";
import OnboardingPanel from "./OnboardingPanel.vue";

class UserOnboarding {
	constructor({ title, steps, wrapper, header_icon }) {
		this.title = title;
		this.steps = steps;
		this.$wrapper = $(wrapper);
		this.header_icon = header_icon;
		this.init();
	}

	init() {
		addStyles();

		let title = this.title || __("Welcome to Frappe!");
		let onboarding_checklist = this.steps || [];
		let header_icon = this.header_icon;

		const app = createApp({
			components: { OnboardingPanel },

			setup() {
				const showPanel = ref(true);
				const steps = ref(onboarding_checklist);
				return () =>
					h(OnboardingPanel, {
						modelValue: showPanel.value,
						title: title,
						steps: steps.value,
						minimizeIcon: frappe.utils.icon("minimize-2", "sm"),
						closeIcon: frappe.utils.icon("close", "sm"),
						headerIcon: header_icon,
						checklistIcon: frappe.utils.icon("circle-check", "sm"),
						completeChecklistIcon: frappe.utils.icon(
							"circle-check",
							"sm",
							"",
							"",
							"",
							"",
							"var(--green)"
						),
						"onUpdate:modelValue": (v) => (showPanel.value = v),
					});
			},
		});

		SetVueGlobals(app);
		app.mount(this.$wrapper.get(0));
	}
}

function addStyles() {
	if (document.getElementById("user-onboarding-styles")) return;

	const style = document.createElement("style");
	style.id = "user-onboarding-styles";

	style.innerHTML = `
	.onb-panel {
		position: fixed;
		right: 24px;
		bottom: 24px;
		width: 380px;
		max-height: 80vh;
		background: #fff;
		border-radius: 16px;
		box-shadow: 0 12px 40px rgba(0,0,0,0.15);
		padding: 16px;
		z-index: 9999;
		display: flex;
		flex-direction: column;
	  }

	.onb-header-main {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 6px;
	}

	.onb-header-left {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.onb-header-icon {
		width: 24px;
		height: 24px;
	}

	.onb-header-title {
		margin: 0;
		font-size: 20px;
		font-weight: 600;
	}

	.onb-header-actions button {
		border: none;
		background: transparent;
		cursor: pointer;
		margin-left: 2px;
	}

	.onb-step-left {
		display: flex;
		align-items: center;
		gap: 8px;
		flex: 1;              /* takes remaining space */
		min-width: 0;         /* allows truncation */
	  }

	.onb-step-title {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.onb-step-icon {
		margin-bottom: 2px;
		align-items: center;
	}

	.onb-step-text {
		white-space: nowrap;
		margin-top: 2px;
		text-align: left;
		font-size: 14px;
	}

	.onb-progress {
		height: 6px;
		background: #eee;
		border-radius: 4px;
		margin: 12px 0;
	}

	.onb-progress-label {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 13px;
		color: #6b7280;
		margin-top: 6px;
	}

	.onb-skip {
		color: #6b7280;
		cursor: pointer;
		font-weight: 500;
	}

	.onb-skip:hover {
		color: #111827;
	}

	.onboarding-progress-bar {
		height: 100%;
		background: #ffcd78;
		border-radius: 4px;
	}

	.onb-steps {
		margin-top: 16px;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 12px;
		align-items: flex-start;
	}

	.onb-group:hover {
		color: #111827;
		background: #f5f5f5;
	}

	.onb-cursor-disabled {
		cursor: not-allowed;
	}

	.onb-select-cursor {
		cursor: pointer;
	}

	.onb-show-on-hover {
		opacity: 0;
		visibility: hidden;
		transition: opacity 0.2s ease;
	}

	.onb-group:hover .onb-show-on-hover {
		opacity: 1;
		visibility: visible;
	}

	.onb-header-logo {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.onb-header-logo img {
		width: 24px;
		height: 24px;
	}

	.onb-header-logo h4 {
		margin: 0;
		white-space: nowrap;
	}
	`;

	document.head.appendChild(style);
}

frappe.provide("frappe.ui");
frappe.ui.UserOnboarding = UserOnboarding;
export default UserOnboarding;
