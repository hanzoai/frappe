context("Navigation", () => {
	before(() => {
<<<<<<< HEAD
		cy.visit("/login");
		cy.login();
		cy.visit("/app/website");
	});
	it("Navigate to route with hash in document name", () => {
		cy.insert_doc(
			"Client Script",
			{
				__newname: "ABC#123",
				dt: "User",
				script: "console.log('ran')",
				enabled: 0,
			},
			true
		);
		cy.visit(`/app/client-script/${encodeURIComponent("ABC#123")}`);
		cy.title().should("eq", "ABC#123");
=======
		cy.login();
	});
	it("Navigate to route with hash in document name", () => {
		cy.insert_doc("ToDo", {
			__newname: "ABC#123",
			description: "Test this",
			ignore_duplicate: true,
		});
		cy.visit("/app/todo/ABC#123");
		cy.title().should("eq", "Test this - ABC#123");
		cy.get_field("description", "Text Editor").contains("Test this");
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		cy.go("back");
		cy.title().should("eq", "Website");
	});

<<<<<<< HEAD
	it("Navigate to previous page after login", () => {
=======
	it.only("Navigate to previous page after login", () => {
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		cy.visit("/app/todo");
		cy.get(".page-head").findByTitle("To Do").should("be.visible");
		cy.clear_filters();
		cy.call("logout");
		cy.reload().as("reload");
		cy.get("@reload").get(".page-card .btn-primary").contains("Login").click();
		cy.location("pathname").should("eq", "/login");
		cy.login();
		cy.reload().as("reload");
		cy.location("pathname").should("eq", "/app/todo");
	});
});
