import axios from "axios";

const state = {
  issues: [],
  editedIssueId: null,
};

const getters = {
  allIssues: (state) => state.issues.sort((a, b) => a.issue_id > b.issue_id ? 1 : -1),
  editedIssueId: (state) => state.editedIssueId,
  editedIssue: (state, getters) =>
    state.issues.filter((issue) => issue.issue_id === getters.editedIssueId)[0],
};

const actions = {
  async fetchIssues({ commit }) {
    const response = await axios.get("http://localhost:5000/api/issues");
    commit("setIssues", response.data.issues);
  },
  async addIssue({ commit }, issue) {
    const response = await axios.post("http://localhost:5000/api/issues", issue);
    commit("newIssue", response.data.issue);
  },
  async deleteIssue({ commit }, id) {
    await axios.delete(`http://localhost:5000/api/issues/${id}`);
    commit("removeIssue", id);
  },
  async updateIssue({ commit }, issue) {
    const response = await axios.put(
      `http://localhost:5000/api/issues/${issue.issue_id}`,
      issue
    );
    commit("updateIssue", response.data.issue);
  },
  editIssue({ commit }, id) {
    commit("setEditedIssueId", id);
  },
  cancelEditIssue({ commit }) {
    commit("clearEditedIssueId");
  },
};

const mutations = {
  setIssues: (state, issues) => (state.issues = issues),
  newIssue: (state, issue) => state.issues.push(issue),
  removeIssue: (state, id) =>
    (state.issues = state.issues.filter((issue) => issue.issue_id !== id)),
  updateIssue: (state, updatedIssue) => {
    const index = state.issues.findIndex((issue) => issue.issue_id === updatedIssue.issue_id);
    if (index !== -1) {
      state.issues.splice(index, 1, updatedIssue);
    }
  },
  setEditedIssueId: (state, id) => (state.editedIssueId = id),
  clearEditedIssueId: (state) => (state.editedIssueId = null),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
