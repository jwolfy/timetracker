<template>
  <div class="container single-task">
    <div class="task-edit-button">
      <b-button
        @click="editTaskById(task.id)"
        size="is-small is-text"
        icon-right="edit"
      >
      </b-button>
    </div>
    <div class="task-comment">
      {{ task.comment }}
    </div>
    <div class="task-duration-formatted has-text-grey-light">
      {{ formatSecondsToTime(task.duration, task.id) }}
    </div>
    <div class="task-duration">
      {{ secondsToHours(task.duration) }}
    </div>
    <div class="task-start-button">
      <b-button
        v-if="isTimerRunningForTask(task.id)"
        size="is-small is-text rounded"
        type="is-danger"
        icon-right="stop"
        @click="stopTimer"
      ></b-button>
      <b-button
        v-else
        size="is-small is-text rounded"
        type="is-success is-light"
        icon-right="play"
        @click="startTask(task.id)"
      ></b-button>
    </div>
  </div>
</template>

<script>
import { secondsToHours, formatTime } from "@/service/utils";
import { mapActions, mapGetters } from "vuex";

export default {
  props: { task: Object },
  computed: {
    ...mapGetters(["isTimerRunningForTask", "editedTaskId", "timer"]),
  },
  methods: {
    ...mapActions(["startTimer", "stopTimer", "editTask"]),
    secondsToHours: secondsToHours,
    startTask(id) {
      this.startTimer(id);
    },
    editTaskById(id) {
      this.editTask(id);
    },
    formatSecondsToTime(seconds, taskId) {
      if (this.isTimerRunningForTask(taskId)) {
        seconds += this.timer.elapsed;
      }
      return formatTime(seconds);
    },
  },
};
</script>

<style scoped>
.single-task {
  display: flex;
  align-items: center;
}

.task-edit-button {
  flex: 1;
  opacity: 0;
}

.task-comment {
  flex: 15;
}

.task-duration-formatted {
  flex: 2;
}

.task-duration {
  flex: 1;
}

.task-start-button {
  flex: 1;
}

.single-task:hover .task-edit-button {
  opacity: 0.7;
}
</style>
