frappe.provide("frappe.ui");

frappe.ui.Scanner = class Scanner {
	constructor(options) {
		this.dialog = null;
		this.handler = null;
		this.options = options;
		this.is_alive = false;

		if (!("multiple" in this.options)) {
			this.options.multiple = false;
		}
		if (options.container) {
			this.$scan_area = $(options.container);
			this.scan_area_id = frappe.dom.set_unique_id(this.$scan_area);
		}
		if (options.dialog) {
			this.dialog = this.make_dialog();
			this.dialog.show();
		}
	}

	scan() {
		this.load_lib().then(() => this.start_scan());
	}

	start_scan() {
		if (!this.handler) {
			this.handler = new Html5Qrcode(this.scan_area_id); // eslint-disable-line
		}
		this.handler
			.start(
				{ facingMode: "environment" },
				{ fps: 10, qrbox: 250 },
				(decodedText, decodedResult) => {
					if (this.options.on_scan) {
						try {
							this.options.on_scan(decodedResult);
						} catch (error) {
<<<<<<< HEAD
							console.error(error);
=======
							console.error(error); // eslint-disable-line
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
						}
					}
					if (!this.options.multiple) {
						this.stop_scan();
						this.hide_dialog();
					}
				},
				(errorMessage) => {
<<<<<<< HEAD
=======
					// eslint-disable-line
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
					// parse error, ignore it.
				}
			)
			.catch((err) => {
				this.is_alive = false;
				this.hide_dialog();
<<<<<<< HEAD
				console.error(err);
=======
				console.error(err); // eslint-disable-line
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			});
		this.is_alive = true;
	}

	stop_scan() {
		if (this.handler && this.is_alive) {
			this.handler.stop().then(() => {
				this.is_alive = false;
				this.$scan_area.empty();
				this.hide_dialog();
			});
		}
	}

	make_dialog() {
		let dialog = new frappe.ui.Dialog({
			title: __("Scan QRCode"),
			fields: [
				{
					fieldtype: "HTML",
					fieldname: "scan_area",
				},
			],
			on_page_show: () => {
				this.$scan_area = dialog.get_field("scan_area").$wrapper;
				this.$scan_area.addClass("barcode-scanner");
				this.scan_area_id = frappe.dom.set_unique_id(this.$scan_area);
				this.scan();
			},
			on_hide: () => {
				this.stop_scan();
			},
		});
		return dialog;
	}

	hide_dialog() {
		this.dialog && this.dialog.hide();
	}

	load_lib() {
<<<<<<< HEAD
		return frappe.require("/assets/frappe/node_modules/html5-qrcode/html5-qrcode.min.js");
=======
		return frappe.require("/assets/frappe/node_modules/html5-qrcode/dist/html5-qrcode.min.js");
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	}
};
