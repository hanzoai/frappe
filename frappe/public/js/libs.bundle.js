import "./jquery-bootstrap";
<<<<<<< HEAD
=======
import Vue from "vue/dist/vue.esm.js";
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
import "./lib/moment";
import "../js/lib/leaflet/leaflet.js";
import "../js/lib/leaflet_easy_button/easy-button.js";
import "../js/lib/leaflet_draw/leaflet.draw.js";
import "../js/lib/leaflet_control_locate/L.Control.Locate.js";
import Sortable from "sortablejs";

<<<<<<< HEAD
window.SetVueGlobals = (app) => {
	app.config.globalProperties.__ = window.__;
	app.config.globalProperties.frappe = window.frappe;
};
=======
window.Vue = Vue;
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
window.Sortable = Sortable;
