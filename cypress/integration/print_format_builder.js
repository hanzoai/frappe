// Generic create-flow coverage for the Print Format Builder (the page
// formerly named "print-format-builder-beta" and renamed in this PR).
// Uses ToDo as the test doctype so the suite has no fixture dependency.

const PF_NAME = `Cypress PF ${Date.now()}`;

context("Print Format Builder — create flow", () => {
	before(() => {
		cy.login();
		cy.visit("/desk");
	});

	after(() => {
		// best-effort cleanup
		cy.window()
			.its("frappe.csrf_token")
			.then((csrf_token) => {
				cy.request({
					method: "DELETE",
					url: `/api/resource/Print Format/${encodeURIComponent(PF_NAME)}`,
					headers: { "X-Frappe-CSRF-Token": csrf_token },
					failOnStatusCode: false,
				});
			});
	});

	// 1. Visiting the page surfaces the Create/Edit dialog
	it("shows the Create or Edit Print Format dialog", () => {
		cy.visit("/app/print-format-builder");
		cy.get_open_dialog().should("contain", "Create or Edit Print Format");
		cy.get_open_dialog().find(".btn-primary").should("contain", "Create");
	});

	// 2. Filling the form and clicking Create persists a beta format
	it("creating a new format inserts a Print Format with print_format_builder_beta=1", () => {
		cy.intercept("POST", "/api/method/frappe.client.insert").as("insert");

		cy.visit("/app/print-format-builder");
		cy.get_open_dialog().should("be.visible");

		cy.fill_field("doctype", "ToDo", "Link");
		cy.fill_field("print_format_name", PF_NAME, "Data");

		cy.get_open_dialog().find(".btn-primary").contains("Create").click();

		// the dialog calls frappe.db.insert -> /api/method/frappe.client.insert
		cy.wait("@insert").its("response.statusCode").should("eq", 200);

		// flag was persisted on the doctype
		cy.window().then((win) => {
			return cy
				.wrap(
					win.frappe.db.get_value("Print Format", PF_NAME, [
						"print_format_builder_beta",
						"doc_type",
					])
				)
				.then(({ message }) => {
					expect(Number(message.print_format_builder_beta)).to.equal(1);
					expect(message.doc_type).to.equal("ToDo");
				});
		});
	});

	// 3. After create, the builder loads for that format and Save persists changes
	it("redirects to the builder for the new format and Save persists a margin change", () => {
		cy.visit(`/app/print-format-builder/${encodeURIComponent(PF_NAME)}`);

		// builder mounts the Vue component — the sidebar with "Page Margins" appears
		cy.contains(".sidebar-menu h5", "Page Margins", { timeout: 20000 }).should("be.visible");

		// change Top margin to 9
		cy.contains(".margin-controls label", "Top")
			.closest(".form-group")
			.find('input[type="number"]')
			.clear()
			.type("9")
			.blur();

		// dirty indicator shows
		cy.get(".indicator-pill.orange", { timeout: 5000 }).should("contain", "Not Saved");

		// Save via the page's primary action
		cy.intercept("POST", "/api/method/frappe.client.save").as("save");
		cy.get(".page-actions .primary-action").contains("Save").click({ force: true });
		cy.wait("@save").its("response.statusCode").should("eq", 200);

		// indicator clears
		cy.get(".indicator-pill.orange").should("not.exist");

		// new value is on the doctype
		cy.window().then((win) => {
			return cy
				.wrap(win.frappe.db.get_value("Print Format", PF_NAME, "margin_top"))
				.then(({ message }) => {
					expect(Number(message.margin_top)).to.equal(9);
				});
		});
	});
});
