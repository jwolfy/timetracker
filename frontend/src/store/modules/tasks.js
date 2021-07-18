import axios from "axios";

const state = {
  tasks: [],
};

const getters = {
  tasksForRange: (state) => state.tasks,
  groupedTasks: (state, getters, rootState) => {
    return state.tasks.reduce((existingData, task) => {
      const spent_on = task["spent_on"];
      const issue_id = task["issue_id"];
      const issue = rootState.issues.issues.filter(
        (issue) => issue.issue_id === issue_id
      )[0];

      const existingDateData = existingData[spent_on] || {}
      const existingIssueIdData = existingDateData[issue_id] || {}
      const existingTasks = existingIssueIdData.tasks || []

      existingTasks.push(task);

      existingIssueIdData.issue = issue
      existingIssueIdData.tasks = existingTasks

      existingDateData[issue_id] = existingIssueIdData
      existingData[spent_on] = existingDateData

      return existingData;
    }, {});
  },
};

const actions = {
  async fetchTasks({ commit }, { startDate, endDate }) {
    const response = await axios.get("http://localhost:5000/api/tasks", {
      params: { start_date: startDate, end_date: endDate },
    });
    commit("setTasks", response.data.tasks);
  },
};

const mutations = {
  setTasks: (state, tasks) => (state.tasks = tasks),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
