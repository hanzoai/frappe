const DOCTYPE = "DocType";
const LIST_URL = "/desk/List/DocType/List";

// Helper — open List View Settings modal for the current list
function openListSettings() {
	cy.get(".menu-btn-group button").click({ force: true });
	cy.get(".dropdown-menu li").filter(":visible").contains("List Settings").click();
	cy.get(".modal-dialog").should("contain", `${DOCTYPE} List View Settings`);
}

// Helper — reset List View Settings for DOCTYPE so each test starts clean
function resetListViewSettings() {
	cy.call("frappe.desk.doctype.list_view_settings.list_view_settings.save_listview_settings", {
		doctype: DOCTYPE,
		listview_settings: { fields: "" },
		removed_listview_fields: [],
	});
}

// Helper — get the rendered pixel width of a list-row-col by fieldname
function getColumnWidth(fieldname) {
	return cy
		.get(`.list-row-head .list-row-col[data-fieldname="${fieldname}"]`)
		.invoke("outerWidth");
}

context("List View — Column Widths", () => {
	before(() => {
		cy.login();
		cy.visit("/desk/website");
	});

	beforeEach(() => {
		resetListViewSettings();
		cy.visit(LIST_URL);
		cy.wait(500);
		cy.clear_filters();
	});

	// ─── 1. DocField width is applied ───────────────────────────────────────────

	it("applies width defined in DocField to the column", () => {
		// Set a known width on the DocType's 'module' field via the API
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "200",
		});

		cy.reload();
		cy.wait(500);

		getColumnWidth("module").should("be.closeTo", 200, 10);

		// Cleanup — remove the width so other tests aren't affected
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "",
		});
	});

	// ─── 2. Width set via List View Settings is applied ─────────────────────────

	it("saves and applies column width set in List View Settings", () => {
		openListSettings();

		// Find the 'module' field row and set width to 180
		cy.get(".fields_order")
			.filter('[data-fieldname="module"]')
			.find("input.form-control")
			.clear()
			.type("180");

		cy.findByRole("button", { name: "Save" }).click();
		cy.wait(500);

		getColumnWidth("module").should("be.closeTo", 180, 10);
	});

	// ─── 3. Width is persisted after page reload ─────────────────────────────────

	it("persists column width across page reloads", () => {
		// Save width 220 via settings
		cy.call(
			"frappe.desk.doctype.list_view_settings.list_view_settings.save_listview_settings",
			{
				doctype: DOCTYPE,
				listview_settings: {
					fields: JSON.stringify([
						{ fieldname: "name", label: "Name" },
						{ fieldname: "module", label: "Module", width: 220 },
					]),
				},
				removed_listview_fields: [],
			}
		);

		cy.reload();
		cy.wait(500);

		getColumnWidth("module").should("be.closeTo", 220, 10);
	});

	// ─── 4. Drag-to-resize changes the column width ──────────────────────────────

	it("drag-to-resize handle changes column width", () => {
		// Get starting width of the module column
		getColumnWidth("module").then((initialWidth) => {
			const dragBy = 80; // drag 80px to the right

			cy.get('.list-row-head .list-row-col[data-fieldname="module"] .list-col-resize-handle')
				.trigger("mousedown", { button: 0, clientX: 0 })
				.trigger("mousemove", { clientX: dragBy }, { bubbles: true })
				.trigger("mouseup", { clientX: dragBy }, { bubbles: true });

			cy.wait(300);

			getColumnWidth("module").should("be.greaterThan", initialWidth + 40);
		});
	});

	// ─── 5. Drag-to-resize width is saved to List View Settings ─────────────────

	it("drag-to-resize width is persisted in List View Settings", () => {
		const dragBy = 60;

		getColumnWidth("module").then((initialWidth) => {
			cy.get('.list-row-head .list-row-col[data-fieldname="module"] .list-col-resize-handle')
				.trigger("mousedown", { button: 0, clientX: 0 })
				.trigger("mousemove", { clientX: dragBy }, { bubbles: true })
				.trigger("mouseup", { clientX: dragBy }, { bubbles: true });

			cy.wait(500);

			// Reload and confirm the new width survived
			cy.reload();
			cy.wait(500);

			getColumnWidth("module").should("be.greaterThan", initialWidth + 30);
		});
	});

	// ─── 6. Min-width constraint (50 px) is enforced ─────────────────────────────

	it("enforces minimum column width of 50 px when dragging", () => {
		// Drag far to the left to attempt collapsing the column below 50 px
		cy.get('.list-row-head .list-row-col[data-fieldname="module"] .list-col-resize-handle')
			.trigger("mousedown", { button: 0, clientX: 500 })
			.trigger("mousemove", { clientX: -500 }, { bubbles: true })
			.trigger("mouseup", { clientX: -500 }, { bubbles: true });

		cy.wait(300);

		getColumnWidth("module").should("be.gte", 50);
	});

	// ─── 7. Max-width constraint (400 px) is enforced ────────────────────────────

	it("enforces maximum column width of 400 px when dragging", () => {
		cy.get('.list-row-head .list-row-col[data-fieldname="module"] .list-col-resize-handle')
			.trigger("mousedown", { button: 0, clientX: 0 })
			.trigger("mousemove", { clientX: 2000 }, { bubbles: true })
			.trigger("mouseup", { clientX: 2000 }, { bubbles: true });

		cy.wait(300);

		getColumnWidth("module").should("be.lte", 400);
	});

	// ─── 8. Resize handle is visible in the header ───────────────────────────────

	it("shows resize handles in the list header", () => {
		cy.get(".list-row-head .list-col-resize-handle").should("have.length.greaterThan", 0);
	});

	// ─── 9. List View Settings dialog shows Width column header ──────────────────

	it("shows Width (px) column header and info icon in List View Settings", () => {
		openListSettings();

		cy.get(".modal-dialog").should("contain", "Width (px)");
		// info icon tooltip is present
		cy.get(".modal-dialog [title]")
			.filter((_, el) => el.title.toLowerCase().includes("drag"))
			.should("exist");

		cy.get(".modal-dialog .btn-modal-close").click();
	});

	// ─── 10. List View Settings priority over DocField width ─────────────────────

	it("List View Settings width takes priority over DocField width", () => {
		// Set DocField width to 150
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "150",
		});

		// Override with 260 in List View Settings
		cy.call(
			"frappe.desk.doctype.list_view_settings.list_view_settings.save_listview_settings",
			{
				doctype: DOCTYPE,
				listview_settings: {
					fields: JSON.stringify([
						{ fieldname: "name", label: "Name" },
						{ fieldname: "module", label: "Module", width: 260 },
					]),
				},
				removed_listview_fields: [],
			}
		);

		cy.reload();
		cy.wait(500);

		// Should be closer to 260 than 150
		getColumnWidth("module").should("be.closeTo", 260, 15);

		// Cleanup
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "",
		});
	});
});
