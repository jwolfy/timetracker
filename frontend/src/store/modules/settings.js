import axios from "axios";

const state = {
  settings: {
    redmine_url: "",
  },
};

const getters = {
  settings: (state) => state.settings,
  redmine_url: (state) =>
    state.settings.redmine_url !== ""
      ? state.settings.redmine_url.replace(/\/$/, "") + "/issues/"
      : "",
};

const actions = {
  async fetchSettings({ commit }) {
    const response = await axios.get("settings");
    commit("setSettings", response.data.settings);
  },
  async saveSettings({ commit }, settings) {
    const response = await axios.post("settings", settings);
    commit("setSettings", response.data.settings);
  },
};

const mutations = {
  setSettings: (state, settings) => (state.settings = settings),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
