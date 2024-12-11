// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {

	if(frappe.utils.get_url_arg('subject')) {
	  $('[name="subject"]').val(frappe.utils.get_url_arg('subject'));
	}

	$('.btn-send').off("click").on("click", function() {
		var email = $('[name="email"]').val();
		var message = $('[name="message"]').val();

		if(!(email && message)) {
			frappe.msgprint('{{ _("Please enter both your email and message so that we can get back to you. Thanks!") }}');
			return false;
		}

		if(!validate_email(email)) {
			frappe.msgprint('{{ _("You seem to have written your name instead of your email. Please enter a valid email address so that we can get back.") }}');
			$('[name="email"]').focus();
			return false;
		}

		$("#contact-alert").toggle(false);
<<<<<<< HEAD
		frappe.call({
			type: "POST",
			method: "frappe.www.contact.send_message",
			args: {
				subject: $('[name="subject"]').val(),
				sender: email,
				message: message,
			},
=======
		frappe.send_message({
			subject: $('[name="subject"]').val(),
			sender: email,
			message: message,
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
			callback: function(r) {
				if (!r.exc) {
					frappe.msgprint('{{ _("Thank you for your message") }}', '{{ _("Message Sent") }}');
				}
				$(':input').val('');
<<<<<<< HEAD
			},
		});
	});
=======
			}
		}, this);
		return false;
	});

>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
