// import axios from "axios";

const state = {
  issues: [
    {
      is_active: true,
      issue_id: 4311,
      subject: "Skype meetings/discussions",
    },
    {
      is_active: true,
      issue_id: 4316,
      subject: "Tickers updates",
    },
    {
      is_active: true,
      issue_id: 5789,
      subject: "Adhoc issues",
    },
    {
      is_active: true,
      issue_id: 9206,
      subject: "Velacroix.com",
    },
  ],
};

const getters = {
  allIssues: (state) => state.issues,
};

const actions = {};

const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
