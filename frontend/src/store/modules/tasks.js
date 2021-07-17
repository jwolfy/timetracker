import axios from "axios";

const state = {
  tasks: [],
};

const getters = {
  tasksForRange: (state) => state.tasks,
  groupedTasks: (state, getters, rootState) => {
    return state.tasks.reduce((accumulator, task) => {
      const spent_on = task["spent_on"];
      const issue_id = task["issue_id"];
      const issue = rootState.issues.issues.filter(
        (issue) => issue.issue_id === issue_id
      )[0];
      const issueData = {
        [issue_id]: Object.assign(accumulator[issue_id] || {}, {
          issue: issue != undefined ? issue : null,
          tasks: (
            (accumulator[issue_id] || { tasks: [] })["tasks"] || []
          ).concat(task),
        }),
      };
      const dateData = {
        [spent_on]: Object.assign(accumulator[spent_on] || {}, issueData),
      };
      return Object.assign(accumulator, dateData);
    }, {});
  },
};

const actions = {
  async fetchTasks({ commit }, { startDate, endDate }) {
    console.log(startDate);
    console.log(endDate);
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
