frappe.provide("frappe.ui");

// icon, title, message, condition, primary_action_label, primary_action
frappe.ui.SidebarCard = class SidebarCard {
	constructor(opts) {
		Object.assign(this, opts);
		this.make(opts);
		this.setup();
		this.set_styles();
	}
	make() {
		if (!this.icon) {
			this.icon = "info";
		}
		this.card = $(
			frappe.render_template("sidebar_card", {
				card: this,
			})
		);

		this.card.prependTo(this.parent);
	}
	setup() {
		this.setup_primary_action();
	}
	setup_primary_action() {
		const me = this;
		this.card.find(".sidebar-card-button").on("click", function (event) {
			event.preventDefault();
			me.primary_action(event);
		});
	}
	set_styles() {
		const $root = $(":root");
		for (const [variable, value] of Object.entries(this.styles)) {
			$root.css(`--${variable}`, value);
		}
	}
};
