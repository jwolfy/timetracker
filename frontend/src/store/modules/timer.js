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
  timerTaskId: (state) => state.timer.task_id,
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
  async startTimer({ commit, getters, dispatch }, taskId) {
    const response = await axios.post("timer", {
      task_id: taskId,
    });
    const previousTaskId = getters.timerTaskId;
    if (previousTaskId != null) {
      dispatch("getTask", previousTaskId);
    }
    commit("setTimer", response.data.timer);
    commit("stopCounter");
    commit("startCounter");
  },
  async stopTimer({ commit, getters, dispatch }) {
    const taskId = getters.timerTaskId;
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
      state.timer.elapsed = ((Date.now() / 1000) | 0) - state.timer.started_at;
    }, 1000)),
  stopCounter: (state) => clearInterval(state.timerInterval),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
