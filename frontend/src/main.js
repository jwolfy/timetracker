import Vue from "vue";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Axios from "axios";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

Vue.config.productionTip = false;

Vue.use(Buefy, {
  defaultIconPack: "fas",
});

Vue.prototype.$http = Axios;
const token = localStorage.getItem("token");
if (token) {
  Vue.prototype.$http.defaults.headers.common["X-Access-Token"] = token;
}

Vue.prototype.$http.interceptors.response.use(null, function(err) {
  return new Promise(function() {
    console.log("intercepted!");
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
