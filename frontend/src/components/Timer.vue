<template>
  <div>
    <div class="task-comment" v-if="timer.task">
      {{ timer.task.comment }}
    </div>
    <div class="time" v-if="timer.is_running">
      {{ formatTimer }}
      <br />
      <b-button
        size="rounded"
        type="is-danger is-light"
        icon-right="stop"
        @click="stopTimer"
      >
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      timerInterval: null,
      elapsedSeconds: 0,
      isRunning: false,
    };
  },
  methods: {
    ...mapActions(["fetchTimer", "stopTimer"]),
  },
  computed: {
    ...mapGetters(["timer"]),
    formatTimer() {
      let hours = Math.floor(this.timer.elapsed / 3600)
        .toString()
        .padStart(2, "0");
      let minutes = Math.floor((this.timer.elapsed - hours * 3600) / 60)
        .toString()
        .padStart(2, "0");
      let seconds =
        this.timer.elapsed -
        (hours * 3600 + minutes * 60).toString().padStart(2, "0");

      return `${hours} : ${minutes} : ${seconds}`;
    },
  },
  created() {
    this.fetchTimer();
  },
};
</script>
