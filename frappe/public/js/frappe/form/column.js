export default class Column {
	constructor(section, df) {
		if (!df) df = {};

		this.df = df;
		this.section = section;
<<<<<<< HEAD
		this.section.columns.push(this);
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		this.make();
		this.resize_all_columns();
	}

	make() {
		this.wrapper = $(`
<<<<<<< HEAD
			<div class="form-column" data-fieldname="${this.df.fieldname}">
				<form>
				</form>
			</div>
		`).appendTo(this.section.body);

		this.form = this.wrapper.find("form").on("submit", () => false);

		if (this.df.description) {
			$(`
				<p class="col-sm-12 form-column-description">
					${__(this.df.description)}
				</p>
			`).prependTo(this.wrapper);
		}

		if (this.df.label) {
			$(`
				<label class="column-label">
					${__(this.df.label, null, this.df.parent)}
				</label>
			`).prependTo(this.wrapper);
=======
			<div class="form-column">
				<form>
				</form>
			</div>
		`)
			.appendTo(this.section.body)
			.find("form")
			.on("submit", function () {
				return false;
			});

		if (this.df.label) {
			$(`
				<label class="control-label">
					${__(this.df.label)}
				</label>
			`).appendTo(this.wrapper);
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
		}
	}

	resize_all_columns() {
		// distribute all columns equally
		let columns = this.section.wrapper.find(".form-column").length;
		let colspan = cint(12 / columns);

		if (columns == 5) {
			colspan = 20;
		}

		this.section.wrapper
			.find(".form-column")
			.removeClass()
			.addClass("form-column")
			.addClass("col-sm-" + colspan);
	}

<<<<<<< HEAD
	add_field() {}

=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	refresh() {
		this.section.refresh();
	}
}
