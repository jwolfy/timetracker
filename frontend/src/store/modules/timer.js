import axios from "axios";

const state = {
  timer: {
    elapsed: 0,
    is_running: false,
    started_at: 0,
    task_id: null,
  },
};

const getters = {
  timer: (state) => state.timer,
  isTimerRunning: (state) => state.timer.is_running,
  isTimerRunningForTask: (state) => (id) =>
    state.timer.is_running && state.timer.task_id === id,
};

const actions = {
  async fetchTimer({ commit }) {
    const response = await axios.get("http://localhost:5000/api/timer");
    commit("setTimer", response.data.timer);
  },
  async startTimer({ commit }, taskId) {
    const response = await axios.post("http://localhost:5000/api/timer", {
      task_id: taskId,
    });
    commit("setTimer", response.data.timer);
  },
  async stopTimer({ commit }) {
    const response = await axios.delete("http://localhost:5000/api/timer");
    commit("setTimer", response.data.timer);
  },
};

const mutations = {
  setTimer: (state, timer) => (state.timer = timer),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
