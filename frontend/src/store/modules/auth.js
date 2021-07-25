import axios from "axios";
import { Base64 } from "js-base64";

const state = {
  status: "",
  token: localStorage.getItem("token") || "",
};

const getters = {
  isLoggedIn: (state) => !!state.token,
  authStatus: (state) => state.status,
};

const actions = {
  login({ commit }, user) {
    return new Promise((resolve, reject) => {
      commit("auth_request");
      axios({
        url: "http://api:5000/api/login",
        method: "GET",
        headers: {
          Authorization:
            "Basic " + Base64.encode(`${user.name}:${user.password}`),
        },
      })
        .then((resp) => {
          const token = resp.data.token;
          localStorage.setItem("token", token);
          axios.defaults.headers.common["X-Access-Token"] = token;
          commit("auth_success", token);
          resolve(resp);
        })
        .catch((err) => {
          commit("auth_error");
          localStorage.removeItem("token");
          reject(err);
        });
    });
  },
  logout({ commit }) {
    return new Promise((resolve) => {
      commit("logout");
      localStorage.removeItem("token");
      delete axios.defaults.headers.common["X-Access-Token"];
      resolve();
    });
  },
};

const mutations = {
  auth_request(state) {
    state.status = "loading";
  },
  auth_success(state, token) {
    state.status = "success";
    state.token = token;
  },
  auth_error(state) {
    state.status = "error";
  },
  logout(state) {
    state.status = "";
    state.token = "";
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
