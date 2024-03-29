import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import issues from "./modules/issues";
import tasks from "./modules/tasks";
import timer from "./modules/timer";
import settings from "./modules/settings"

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    issues,
    tasks,
    timer,
    settings,
  },
});
