// This file is used to make sure that `moment` is bound to the window
// before the bundle finishes loading, due to imports (datetime.js) in the bundle
// that depend on `moment`.
<<<<<<< HEAD
import momentTimezone from "moment-timezone/builds/moment-timezone-with-data-10-year-range.min.js";
=======
import momentTimezone from "moment-timezone/builds/moment-timezone-with-data.js";
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
window.moment = momentTimezone;
