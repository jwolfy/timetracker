<template>
  <div>
    {{ timer.task }}
    <br />
    {{ formatTimer }}
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
    ...mapActions(["fetchTimer"]),
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
