<template>
  <div>
    <div class="task-comment" v-if="timer.task">
      {{ timer.task.comment }}
    </div>
    <div class="time" v-if="timer.is_running">
      {{ formatTimer(timer.elapsed) }}
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
import { formatTime } from "@/service/utils";

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
    formatTimer: formatTime,
  },
  computed: {
    ...mapGetters(["timer"]),
  },
  created() {
    this.fetchTimer();
  },
};
</script>
