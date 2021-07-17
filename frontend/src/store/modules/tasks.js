import axios from "axios";

const state = {
  tasks: [],
};

const getters = {
  tasksForRange: (state) => state.tasks,
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
