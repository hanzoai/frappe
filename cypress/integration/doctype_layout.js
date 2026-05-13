import target_doctype from "../fixtures/layout_target_doctype";

const TARGET = target_doctype.name;
const SLUG = TARGET.toLowerCase().replace(/ /g, "-");
const COMPACT = `Compact ${TARGET}`;
const SPECIAL = `Special ${TARGET}`;

// Shared saved doc used across switcher tests (menu is hidden for __islocal docs)
let TEST_DOC_NAME;

context("DocType Layout", () => {
	before(() => {
		cy.login("Administrator");
		cy.visit("/desk");
		cy.insert_doc("DocType", target_doctype, true);

		// Wipe any layouts from a previous run so field rows are deterministic
		cy.remove_doc("DocType Layout", COMPACT, true);
		cy.remove_doc("DocType Layout", SPECIAL, true);

		cy.insert_doc("DocType Layout", {
			name: COMPACT,
			title: "Compact",
			document_type: TARGET,
			fields: [
				{ fieldname: "data1", label: "Compact Data 1" },
				{ fieldname: "data2", hidden: 1 },
				{ fieldname: "is_special" },
				{ fieldname: "description" },
			],
		});

		cy.insert_doc("DocType Layout", {
			name: SPECIAL,
			title: "Special",
			document_type: TARGET,
			condition: "doc.is_special == 1",
			fields: [
				{ fieldname: "data1" },
				{ fieldname: "data2" },
				{ fieldname: "is_special" },
				{ fieldname: "description", label: "Special Notes" },
			],
		});

		// Create a saved doc — the toolbar menu is hidden for __islocal (new) docs
		cy.insert_doc(TARGET, { data1: "switcher-test" }).then((doc) => {
			TEST_DOC_NAME = doc.name;
		});

		// Reload so frappe.boot.doctype_layouts includes the newly created layouts
		cy.visit("/desk");
	});

	it("DocType Layout form: Sync Fields populates rows and Form Builder renders", () => {
		cy.visit(`/desk/doctype-layout/${encodeURIComponent(COMPACT)}`);
		cy.get("body").should("have.attr", "data-ajax-state", "complete");

		// Field rows set via API in before() should already be present
		cy.window()
			.its("cur_frm.doc.fields")
			.should((rows) => {
				const names = rows.map((r) => r.fieldname);
				expect(names).to.include.members(["data1", "data2", "is_special", "description"]);
			});

		// Sync Fields always reports the auto-added `doctype_layout` custom field
		// as "Added: Layout"; wait for that modal, then close it.
		cy.findByRole("button", { name: "Sync Fields" }).click({ force: true });
		cy.get(".modal:visible").should("contain.text", "Synced Fields");
		cy.hide_dialog();

		// frm.dirty() + frm.refresh_field() cause an async re-render; wait for the
		// "Not Saved" pill to appear before querying the tab.
		cy.get(".title-area .indicator-pill").should("contain.text", "Not Saved");
		cy.findByRole("tab", { name: "Parent Layout" }).click();
		cy.get(".form-builder-container").should("exist");
	});

	it("Toolbar switcher pins a layout and applies overrides", () => {
		cy.visit(`/desk/${SLUG}/${TEST_DOC_NAME}`);
		cy.get("body").should("have.attr", "data-ajax-state", "complete");

		// Base meta — Data 1 unmodified, Data 2 visible
		cy.get("[data-fieldname='data1'] .clearfix label").should("contain.text", "Data 1");
		cy.get("[data-fieldname='data2']").should("be.visible");
		cy.get(".layout-indicator").should("not.exist");

		// Open the form menu and pick Compact
		cy.get(".menu-btn-group > .btn").click();
		cy.get(".menu-btn-group .dropdown-menu li").contains("Compact").click();

		cy.get(".layout-indicator").should("contain.text", "Compact");
		// URLSearchParams encodes spaces as '+'; encodeURIComponent uses '%20'.
		// Match either form to stay robust across browser/polyfill differences.
		cy.location("search").should("satisfy", (s) =>
			s.includes(`layout=${COMPACT.replace(/ /g, "+")}`) ||
			s.includes(`layout=${encodeURIComponent(COMPACT)}`)
		);

		// Overrides applied
		cy.get("[data-fieldname='data1'] .clearfix label").should(
			"contain.text",
			"Compact Data 1"
		);
		cy.get("[data-fieldname='data2']").should("not.be.visible");
	});

	it("'Default View' clears the pinned layout", () => {
		cy.visit(`/desk/${SLUG}/${TEST_DOC_NAME}`);
		cy.get(".menu-btn-group > .btn").click();
		cy.get(".menu-btn-group .dropdown-menu li").contains("Compact").click();
		cy.get(".layout-indicator").should("contain.text", "Compact");

		cy.get(".menu-btn-group > .btn").click();
		cy.get(".menu-btn-group .dropdown-menu li").contains("Default View").click();

		cy.get(".layout-indicator").should("not.exist");
		cy.location("search").should("not.include", "layout=");
		cy.get("[data-fieldname='data1'] .clearfix label").should("contain.text", "Data 1");
		cy.get("[data-fieldname='data2']").should("be.visible");
	});

	it("Condition auto-switches the layout after a matching value is saved", () => {
		cy.visit(`/desk/${SLUG}/new`);
		cy.get("body").should("have.attr", "data-ajax-state", "complete");

		// Condition unmet — no layout
		cy.get(".layout-indicator").should("not.exist");

		cy.fill_field("data1", "auto-switch", "Data");
		cy.get("[data-fieldname='is_special'] label").click({ force: true });
		cy.click_doc_primary_button("Save");

		cy.get(".layout-indicator").should("contain.text", "Special");
		cy.location("search").should("satisfy", (s) =>
			s.includes(`layout=${SPECIAL.replace(/ /g, "+")}`) ||
			s.includes(`layout=${encodeURIComponent(SPECIAL)}`)
		);
		cy.get("[data-fieldname='description'] .clearfix label").should(
			"contain.text",
			"Special Notes"
		);
	});
});
