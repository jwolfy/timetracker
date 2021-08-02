<template>
  <div class="card p-2 ml-3" v-if="timer.is_running">
    <div class="task-comment has-text-weight-semibold" v-if="timer.task">
      {{ timer.task.comment }}
    </div>
    <div class="time" v-if="timer.is_running">
      {{ formatTimer(timer.elapsed) }}
      <br />
      <b-button
        size="rounded"
        type="is-danger"
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
