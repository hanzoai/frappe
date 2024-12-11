frappe.ui.form.FormViewers = class FormViewers {
	constructor({ frm, parent }) {
		this.frm = frm;
		this.parent = parent;
		this.parent.tooltip({ title: __("Currently Viewing") });
<<<<<<< HEAD

		this._past_users = {};
		this._active_users = {};
		this.setup_events();
	}

	get past_users() {
		return this._past_users[this.frm?.doc?.name] || [];
	}

	set past_users(users) {
		const docname = this.frm?.doc?.name;
		if (!docname) return;

		this._past_users[docname] = users;
	}

	get active_users() {
		return this._active_users[this.frm?.doc?.name] || [];
	}

	set active_users(users) {
		const docname = this.frm?.doc?.name;
		if (!docname) return;

		this._active_users[docname] = users;
	}

	refresh() {
		if (!this.active_users.length) {
			this.parent.empty();
			return;
		}
		let avatar_group = frappe.avatar_group(this.active_users, 5, {
=======
	}

	refresh() {
		let users = this.frm.get_docinfo()["viewers"];
		if (!users || !users.current || !users.current.length) {
			this.parent.empty();
			return;
		}

		let currently_viewing = users.current.filter((user) => user != frappe.session.user);
		let avatar_group = frappe.avatar_group(currently_viewing, 5, {
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			align: "left",
			overlap: true,
		});
		this.parent.empty().append(avatar_group);
	}
<<<<<<< HEAD

	setup_events() {
		let me = this;
		frappe.realtime.off("doc_viewers");
		frappe.realtime.on("doc_viewers", function (data) {
			me.update_users(data);
		});
	}

	async update_users({ doctype, docname, users = [] }) {
		users = users.filter((u) => u != frappe.session.user);

		const added_users = users.filter((user) => !this.past_users.includes(user));
		const removed_users = this.past_users.filter((user) => !users.includes(user));
		const changed_users = [...added_users, ...removed_users];

		if (changed_users.length === 0) return;

		await this.fetch_user_info(users);

		this.active_users = users;
		this.past_users = users;

		if (this.frm?.doc?.doctype === doctype && this.frm?.doc?.name == docname) {
			this.refresh();
		}
	}

	async fetch_user_info(users) {
		let unknown_users = [];
		for (let user of users) {
			if (!frappe.boot.user_info[user]) unknown_users.push(user);
		}
		if (!unknown_users.length) return;

		const data = await frappe.xcall("frappe.desk.form.load.get_user_info_for_viewers", {
			users: unknown_users,
		});
		Object.assign(frappe.boot.user_info, data);
=======
};

frappe.ui.form.FormViewers.set_users = function (data, type) {
	const doctype = data.doctype;
	const docname = data.docname;
	const docinfo = frappe.model.get_docinfo(doctype, docname);

	const past_users = ((docinfo && docinfo[type]) || {}).past || [];
	const users = data.users || [];
	const new_users = users.filter((user) => !past_users.includes(user));

	if (new_users.length === 0) return;

	const set_and_refresh = () => {
		const info = {
			past: past_users.concat(new_users),
			new: new_users,
			current: users,
		};

		frappe.model.set_docinfo(doctype, docname, type, info);

		if (
			cur_frm &&
			cur_frm.doc &&
			cur_frm.doc.doctype === doctype &&
			cur_frm.doc.name == docname &&
			cur_frm.viewers
		) {
			cur_frm.viewers.refresh(true, type);
		}
	};

	let unknown_users = [];
	for (let user of users) {
		if (!frappe.boot.user_info[user]) unknown_users.push(user);
	}

	if (unknown_users.length === 0) {
		set_and_refresh();
	} else {
		// load additional user info
		frappe
			.xcall("frappe.desk.form.load.get_user_info_for_viewers", { users: unknown_users })
			.then((data) => {
				Object.assign(frappe.boot.user_info, data);
				set_and_refresh();
			});
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
	}
};
