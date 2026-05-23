const DOCTYPE = "DocType";
const LIST_URL = "/desk/List/DocType/List";

// Columns we explicitly configure so every test has a predictable starting state.
// "module" has in_list_view=1 on DocType so it is always available to add.
const BASE_FIELDS = JSON.stringify([
	{ fieldname: "name", label: "Name" },
	{ fieldname: "module", label: "Module" },
]);

// Helper — open List View Settings modal for the current list
function openListSettings() {
	cy.get(".menu-btn-group button").click({ force: true });
	cy.get(".dropdown-menu li").filter(":visible").contains("List Settings").click();
	cy.get(".modal-dialog").should("contain", `${DOCTYPE} List View Settings`);
}

// Helper — reset List View Settings to a clean, known state before each test.
// Pass "[]" (valid JSON) so frappe.parse_json() never receives an empty string.
function resetListViewSettings() {
	cy.call("frappe.desk.doctype.list_view_settings.list_view_settings.save_listview_settings", {
		doctype: DOCTYPE,
		listview_settings: { fields: BASE_FIELDS },
		removed_listview_fields: [],
	});
}

// Helper — get the rendered pixel width of a list-row-col by fieldname
function getColumnWidth(fieldname) {
	return cy
		.get(`.list-row-head .list-row-col[data-fieldname="${fieldname}"]`)
		.invoke("outerWidth");
}

// Helper — simulate a drag-to-resize by dispatching native MouseEvents so that
// jQuery's $(document) listeners (used by setup_column_resize) receive them.
function dragResizeColumn(fieldname, deltaX) {
	cy.window().then((win) => {
		const handle = win.document.querySelector(
			`.list-row-head .list-row-col[data-fieldname="${fieldname}"] .list-col-resize-handle`
		);
		if (!handle) throw new Error(`Resize handle for "${fieldname}" not found`);

		const rect = handle.getBoundingClientRect();
		const startX = rect.left + rect.width / 2;

		handle.dispatchEvent(
			new win.MouseEvent("mousedown", {
				bubbles: true,
				cancelable: true,
				button: 0,
				clientX: startX,
				pageX: startX,
			})
		);

		win.document.dispatchEvent(
			new win.MouseEvent("mousemove", {
				bubbles: true,
				cancelable: true,
				clientX: startX + deltaX,
				pageX: startX + deltaX,
			})
		);

		win.document.dispatchEvent(
			new win.MouseEvent("mouseup", {
				bubbles: true,
				cancelable: true,
				clientX: startX + deltaX,
				pageX: startX + deltaX,
			})
		);
	});
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

	// ─── 1. DocField width is applied ────────────────────────────────────────────

	it("applies width defined in DocField to the column", () => {
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "200",
		});

		cy.reload();
		cy.wait(500);

		getColumnWidth("module").should("be.closeTo", 200, 15);

		// Cleanup
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "",
		});
	});

	// ─── 2. Width set via List View Settings dialog is applied ───────────────────

	it("saves and applies column width set in List View Settings dialog", () => {
		openListSettings();

		cy.get(".fields_order")
			.filter('[data-fieldname="module"]')
			.find("input.form-control")
			.clear()
			.type("180");

		cy.findByRole("button", { name: "Save" }).click();
		cy.wait(500);

		getColumnWidth("module").should("be.closeTo", 180, 15);
	});

	// ─── 3. Width persists after page reload ─────────────────────────────────────

	it("persists column width across page reloads", () => {
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

		getColumnWidth("module").should("be.closeTo", 220, 15);
	});

	// ─── 4. Drag-to-resize changes the column width ──────────────────────────────

	it("drag-to-resize handle changes column width", () => {
		getColumnWidth("module").then((initialWidth) => {
			dragResizeColumn("module", 80);
			cy.wait(300);
			getColumnWidth("module").should("be.greaterThan", initialWidth + 40);
		});
	});

	// ─── 5. Drag-to-resize width is persisted after reload ───────────────────────

	it("drag-to-resize width is persisted in List View Settings", () => {
		getColumnWidth("module").then((initialWidth) => {
			dragResizeColumn("module", 60);
			cy.wait(600);

			cy.reload();
			cy.wait(500);

			getColumnWidth("module").should("be.greaterThan", initialWidth + 30);
		});
	});

	// ─── 6. Min-width constraint (50 px) is enforced ─────────────────────────────

	it("enforces minimum column width of 50 px when dragging", () => {
		dragResizeColumn("module", -2000);
		cy.wait(300);
		getColumnWidth("module").should("be.gte", 50);
	});

	// ─── 7. Max-width constraint (400 px) is enforced ────────────────────────────

	it("enforces maximum column width of 400 px when dragging", () => {
		dragResizeColumn("module", 2000);
		cy.wait(300);
		getColumnWidth("module").should("be.lte", 400);
	});

	// ─── 8. Resize handles are present in the header ─────────────────────────────

	it("shows resize handles in the list header", () => {
		cy.get(".list-row-head .list-col-resize-handle").should("have.length.greaterThan", 0);
	});

	// ─── 9. List View Settings dialog shows Width (px) header and hint ───────────

	it("shows Width (px) column header and drag hint in List View Settings", () => {
		openListSettings();

		cy.get(".modal-dialog").should("contain", "Width (px)");
		cy.get(".modal-dialog [title]")
			.filter((_, el) => el.title.toLowerCase().includes("drag"))
			.should("exist");

		cy.get(".modal-dialog .btn-modal-close").click();
	});

	// ─── 10. List View Settings width takes priority over DocField width ──────────

	it("List View Settings width takes priority over DocField width", () => {
		// DocField says 150 px
		cy.call("frappe.client.set_value", {
			doctype: "DocField",
			filters: { parent: DOCTYPE, fieldname: "module" },
			fieldname: "width",
			value: "150",
		});

		// List View Settings overrides to 260 px
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
