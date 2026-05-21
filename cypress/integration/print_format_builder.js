// Create-flow coverage for the Print Format Builder (the page renamed
// from "print-format-builder-beta" → "print-format-builder" in this PR).
//
// Each test generates its own unique PF_NAME and tears it down in
// afterEach, so Cypress retries don't collide with leftover docs.

context("Print Format Builder — create flow", () => {
	let PF_NAME;

	before(() => {
		cy.login();
		cy.visit("/app");
	});

	beforeEach(() => {
		PF_NAME = `Cypress PF ${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
	});

	afterEach(() => {
		// best-effort cleanup — DELETE swallows 404 / 417 via failOnStatusCode
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

	// 1. Page loads with the Create-or-Edit dialog
	it("shows the Create or Edit Print Format dialog", () => {
		cy.visit("/app/print-format-builder");
		cy.get_open_dialog().should("contain", "Create or Edit Print Format");
		cy.get_open_dialog().find(".btn-primary").should("contain", "Create");
	});

	// 2. Filling the dialog and clicking Create inserts a beta format
	it("creates a new Print Format with print_format_builder_beta=1", () => {
		cy.intercept("POST", "api/method/frappe.client.insert").as("insert");

		cy.visit("/app/print-format-builder");
		cy.get_open_dialog().should("be.visible");
		cy.fill_field("doctype", "ToDo", "Link");
		cy.fill_field("print_format_name", PF_NAME, "Data");
		cy.get_open_dialog().find(".btn-primary").contains("Create").click();

		cy.wait("@insert").its("response.statusCode").should("eq", 200);

		cy.window().then((win) =>
			cy
				.wrap(
					win.frappe.db.get_value("Print Format", PF_NAME, [
						"print_format_builder_beta",
						"doc_type",
					])
				)
				.then(({ message }) => {
					expect(Number(message.print_format_builder_beta)).to.equal(1);
					expect(message.doc_type).to.equal("ToDo");
				})
		);
	});

	// 3. Loading the builder for an existing format and saving a change
	//    (creates the doc via API up-front so this test doesn't depend on #2)
	it("loads the builder and Save persists a margin change", () => {
		cy.insert_doc(
			"Print Format",
			{
				name: PF_NAME,
				doc_type: "ToDo",
				print_format_builder_beta: 1,
			},
			true
		);

		cy.intercept("POST", "api/method/frappe.client.save").as("save");
		cy.visit(`/app/print-format-builder/${encodeURIComponent(PF_NAME)}`);

		// PrintFormatBuilder.vue only renders the subtree once
		// print_format + meta + layout are all loaded — give it time.
		cy.contains(".sidebar-menu h5", "Page Margins", { timeout: 30000 }).should("be.visible");

		// change Top margin to 9
		cy.contains(".margin-controls label", "Top")
			.closest(".form-group")
			.find('input[type="number"]')
			.clear()
			.type("9")
			.blur();

		// dirty pill appears
		cy.get(".indicator-pill.orange", { timeout: 5000 }).should("contain", "Not Saved");

		// Save via the page's primary action
		cy.contains(".page-actions .primary-action", "Save").click({ force: true });
		cy.wait("@save").its("response.statusCode").should("eq", 200);
		cy.get(".indicator-pill.orange").should("not.exist");

		// value persisted
		cy.window().then((win) =>
			cy
				.wrap(win.frappe.db.get_value("Print Format", PF_NAME, "margin_top"))
				.then(({ message }) => {
					expect(Number(message.margin_top)).to.equal(9);
				})
		);
	});
});
