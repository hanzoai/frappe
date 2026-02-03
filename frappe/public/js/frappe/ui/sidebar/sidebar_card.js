frappe.provide("frappe.ui");

// icon, title, message, condition, primary_action_label, primary_action
frappe.ui.SidebarCard = class SidebarCard {
	constructor(opts) {
		Object.assign(this, opts);
		this.make(opts);
	}
	make() {
		this.card = $(
			frappe.render_template("sidebar_card", {
				card: this,
			})
		);

		this.card.prependTo(this.parent);
	}
};
