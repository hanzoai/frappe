class PulseProvider {
	constructor() {
		this.enabled = false;
		this.eq = null;
	}

	is_enabled() {
		return frappe.boot.telemetry_provider?.includes("pulse") && frappe.boot.enable_telemetry;
	}

	init() {
		if (!this.is_enabled()) return;
		this.enabled = true;

		try {
			this.eq = new QueueManager((events) => this.sendEvents(events), {
				flushInterval: 10000,
			});

			// Send remaining events on unload
			window.addEventListener("beforeunload", () => {
				if (this.eq.queue.length) {
					this.sendBeacon(this.eq.queue);
				}
			});
		} catch (error) {
			// ignore errors
		}
	}

	capture(event, app, props) {
		if (!this.enabled) return;

		this.eq.add({
			event_name: event,
			app: app,
			properties: props,
			user: frappe.session.user,
			captured_at: new Date().toISOString(),
		});
	}

	sendEvents(events) {
		try {
			frappe.call({
				method: "frappe.utils.telemetry.pulse.client.bulk_capture",
				args: { events },
				type: "POST",
				no_spinner: true,
				freeze: false,
				error: () => {},
				always: () => {},
			});
		} catch (error) {
			// ignore errors
		}
	}

	sendBeacon(events) {
		try {
			if (navigator.sendBeacon) {
				const url = "/api/method/frappe.utils.telemetry.pulse.client.bulk_capture";
				const data = new FormData();
				data.append("events", JSON.stringify(events));
				navigator.sendBeacon(url, data);
			}
		} catch (error) {
			// ignore errors
		}
	}
}

class QueueManager {
	constructor(flushCallback, options = {}) {
		this.flushCallback = flushCallback;
		this.queue = [];
		this.maxQueueSize = options.maxQueueSize || 20;
		this.flushInterval = options.flushInterval || 5000;
		this.timer = null;

		this.start();
	}

	start() {
		this.timer = setInterval(() => {
			if (this.queue.length) this.flush();
		}, this.flushInterval);
	}

	add(event) {
		this.queue.push(event);

		if (this.queue.length >= this.maxQueueSize) {
			this.flush();
		}
	}

	flush() {
		if (!this.queue.length) return;

		const batch = this.queue.splice(0);
		try {
			this.flushCallback(batch);
		} catch (error) {
			// ignore errors
		}
	}

	stop() {
		if (this.timer) {
			clearInterval(this.timer);
			this.timer = null;
		}
		this.flush();
	}
}

export const pulse_provider = new PulseProvider();
