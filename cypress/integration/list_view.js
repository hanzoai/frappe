context("List View", () => {
	before(() => {
		cy.login();
		cy.visit("/app/website");
		return cy
			.window()
			.its("frappe")
			.then((frappe) => {
				return frappe.xcall("frappe.tests.ui_test_helpers.setup_workflow");
			});
	});

<<<<<<< HEAD
	it("Keep checkbox checked after Refresh", { scrollBehavior: false }, () => {
		cy.go_to_list("ToDo");
		cy.clear_filters();
		cy.get(".list-header-subject > .list-subject > .list-check-all").click();
		cy.get("button[data-original-title='Reload List']").click();
		cy.get(".list-row-container .list-row-checkbox:checked").should("be.visible");
	});

=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	it('enables "Actions" button', { scrollBehavior: false }, () => {
		const actions = [
			"Approve",
			"Reject",
			"Export",
			"Assign To",
<<<<<<< HEAD
			"Clear Assignment",
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			"Apply Assignment Rule",
			"Add Tags",
			"Print",
		];
		cy.go_to_list("ToDo");
		cy.clear_filters();
<<<<<<< HEAD
		cy.get(".list-header-subject > .list-subject > .list-check-all").click();
		cy.findByRole("button", { name: "Actions" }).click();
		cy.get(".dropdown-menu li:visible .dropdown-item")
			.should("have.length", 8)
=======
		cy.get('.list-row-container:contains("Pending") .list-row-checkbox').click({
			multiple: true,
			force: true,
		});
		cy.get(".actions-btn-group button").contains("Actions").should("be.visible").click();
		cy.get(".dropdown-menu li:visible .dropdown-item")
			.should("have.length", 7)
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			.each((el, index) => {
				cy.wrap(el).contains(actions[index]);
			})
			.then((elements) => {
				cy.intercept({
					method: "POST",
					url: "api/method/frappe.model.workflow.bulk_workflow_approval",
				}).as("bulk-approval");
				cy.wrap(elements).contains("Approve").click();
				cy.wait("@bulk-approval");
<<<<<<< HEAD
				cy.hide_dialog();
=======
				cy.wait(300);
				cy.get_open_dialog().find(".btn-modal-close").click();
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
				cy.reload();
				cy.clear_filters();
				cy.get(".list-row-container:visible").should("contain", "Approved");
			});
	});
});
