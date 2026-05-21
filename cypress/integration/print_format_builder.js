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

		// frappe.client.insert returns the inserted doc — inspect it directly
		// rather than round-tripping through frappe.db.get_value (which can
		// strip fields the user can't read in list view).
		cy.wait("@insert").then((interception) => {
			expect(interception.response.statusCode).to.equal(200);
			const doc = interception.response.body.message;
			expect(doc.name).to.equal(PF_NAME);
			expect(doc.doc_type).to.equal("ToDo");
			expect(Number(doc.print_format_builder_beta)).to.equal(1);
		});
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

		// Save via the page's primary action; assert the saved doc reflects
		// the new margin (frappe.client.save returns the persisted doc).
		cy.contains(".page-actions .primary-action", "Save").click({ force: true });
		cy.wait("@save").then((interception) => {
			expect(interception.response.statusCode).to.equal(200);
			expect(Number(interception.response.body.message.margin_top)).to.equal(9);
		});
		cy.get(".indicator-pill.orange").should("not.exist");
	});
});
