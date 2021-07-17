import axios from "axios";

const state = {
  issues: [],
};

const getters = {
  allIssues: (state) => state.issues,
};

const actions = {
  async fetchIssues({ commit }) {
    const response = await axios.get("http://localhost:5000/api/issues");
    commit("setIssues", response.data.issues);
  },
};

const mutations = {
  setIssues: (state, issues) => (state.issues = issues),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
