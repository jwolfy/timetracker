import axios from "axios";

const state = {
  timer: {
    elapsed: 0,
    is_running: false,
    started_at: 0,
    task_id: null,
  },
  timerInterval: null,
};

const getters = {
  timer: (state) => state.timer,
  isTimerRunning: (state) => state.timer.is_running,
  isTimerRunningForTask: (state) => (id) =>
    state.timer.is_running && state.timer.task_id === id,
  timerInterval: (state) => state.timerInterval,
};

const actions = {
  async fetchTimer({ commit, getters }) {
    const response = await axios.get("timer");
    commit("setTimer", response.data.timer);

    if (response.data.timer.is_running && getters.timerInterval == null) {
      commit("stopCounter");
      commit("startCounter");
    }
  },
  async startTimer({ commit }, taskId) {
    const response = await axios.post("timer", {
      task_id: taskId,
    });
    commit("setTimer", response.data.timer);
    commit("stopCounter");
    commit("startCounter");
  },
  async stopTimer({ commit, getters, dispatch }) {
    const taskId = getters.timer.task_id;
    const response = await axios.delete("timer");
    commit("setTimer", response.data.timer);
    commit("stopCounter");
    dispatch("getTask", taskId);
  },
};

const mutations = {
  setTimer: (state, timer) => (state.timer = timer),
  startCounter: (state) =>
    (state.timerInterval = setInterval(() => {
      state.timer.elapsed++;
    }, 1000)),
  stopCounter: (state) => clearInterval(state.timerInterval),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
