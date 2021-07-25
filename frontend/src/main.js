import Vue from "vue";

import Buefy from "buefy";
import "buefy/dist/buefy.css";

import App from "./App.vue";
import router from "./router";
import store from "./store";
import Axios from "axios";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import {
  faCalendarAlt,
  faPlay,
  faStop,
  faTrashAlt,
  faEdit,
  faSearch,
  faAngleLeft,
  faAngleRight,
  faTimesCircle,
  faExclamationCircle,
  faSave,
  faWindowClose,
  faArrowUp,
} from "@fortawesome/free-solid-svg-icons";

// Font Awesome icons
dom.watch();
library.add(
  faCalendarAlt,
  faPlay,
  faStop,
  faTrashAlt,
  faEdit,
  faSearch,
  faAngleLeft,
  faAngleRight,
  faTimesCircle,
  faExclamationCircle,
  faSave,
  faWindowClose,
  faArrowUp,
);

Vue.config.productionTip = false;

Vue.use(Buefy, {
  defaultIconPack: "fas",
  defaultIconComponent: FontAwesomeIcon,
});

// axios
Vue.prototype.$http = Axios;
Vue.prototype.$http.defaults.baseURL = 'http://localhost/api/'
const token = localStorage.getItem("token");
if (token) {
  Vue.prototype.$http.defaults.headers.common["X-Access-Token"] = token;
}

// logout on token expiration
Vue.prototype.$http.interceptors.response.use(null, function(err) {
  return new Promise(function() {
    if (err.response.status === 401) {
      store.dispatch("logout");
      router.push("/login");
    }
  });
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
