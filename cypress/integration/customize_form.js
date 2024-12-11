context("Customize Form", () => {
	before(() => {
		cy.login();
		cy.visit("/app/customize-form");
	});
	it("Changing to naming rule should update autoname", () => {
		cy.fill_field("doc_type", "ToDo", "Link").blur();
<<<<<<< HEAD
		cy.wait(2000);
		cy.findByRole("tab", { name: "Details" }).click();
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		cy.click_form_section("Naming");
		const naming_rule_default_autoname_map = {
			"Set by user": "prompt",
			"By fieldname": "field:",
			Expression: "format:",
			"Expression (old style)": "",
			Random: "hash",
			"By script": "",
		};
		Cypress._.forOwn(naming_rule_default_autoname_map, (value, naming_rule) => {
			cy.fill_field("naming_rule", naming_rule, "Select");
			cy.get_field("autoname", "Data").should("have.value", value);
		});
	});
});
