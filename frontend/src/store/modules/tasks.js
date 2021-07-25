import axios from "axios";

const state = {
  tasks: [],
  editedTaskId: null,
};

const getters = {
  groupedTasks: (state, getters, rootState) => {
    const tasks = state.tasks.reduce((existingData, task) => {
      const spent_on = task["spent_on"];
      const issue_id = task["issue_id"];
      const issue = rootState.issues.issues.filter(
        (issue) => issue.issue_id === issue_id
      )[0];

      const existingDateData = existingData[spent_on] || {};
      const existingIssueIdData = existingDateData[issue_id] || {};
      const existingTasks = existingIssueIdData.tasks || [];

      existingTasks.push(task);

      existingIssueIdData.issue = issue;
      existingIssueIdData.tasks = existingTasks;

      existingDateData[issue_id] = existingIssueIdData;
      existingData[spent_on] = existingDateData;

      return existingData;
    }, {});
    return Object.keys(tasks)
      .sort()
      .reduce((obj, key) => {
        obj[key] = tasks[key];
        return obj;
      }, {});
  },
  editedTaskId: (state) => state.editedTaskId,
  editedTask: (state, getters) =>
    state.tasks.filter((task) => task.id === getters.editedTaskId)[0],
};

const actions = {
  async fetchTasks({ commit }, { startDate, endDate }) {
    const response = await axios.get("http://api:5000/api/tasks", {
      params: { start_date: startDate, end_date: endDate },
    });
    commit("setTasks", response.data.tasks);
  },
  async addTask({ commit }, task) {
    const response = await axios.post("http://api:5000/api/tasks", task);
    commit("newTask", response.data.task);
  },
  async deleteTask({ commit }, id) {
    await axios.delete(`http://api:5000/api/tasks/${id}`);
    commit("removeTask", id);
  },
  async updateTask({ commit }, task) {
    const response = await axios.put(`http://api:5000/api/tasks/${task.id}`, task);
    commit("updateTask", response.data.task);
  },
  async getTask({ commit }, id) {
    const response = await axios.get(`http://api:5000/api/tasks/${id}`)
    commit("updateTask", response.data.task);
  },
  editTask({ commit }, id) {
    commit("setEditedTaskId", id);
  },
  cancelEditTask({ commit }) {
    commit("clearEditedTaskId");
  },
};

const mutations = {
  setTasks: (state, tasks) => (state.tasks = tasks),
  newTask: (state, task) => state.tasks.push(task),
  removeTask: (state, id) =>
    (state.tasks = state.tasks.filter((task) => task.id !== id)),
  updateTask: (state, updatedTask) => {
    const index = state.tasks.findIndex((task) => task.id === updatedTask.id);
    if (index !== -1) {
      state.tasks.splice(index, 1, updatedTask);
    }
  },
  setEditedTaskId: (state, id) => (state.editedTaskId = id),
  clearEditedTaskId: (state) => (state.editedTaskId = null),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
