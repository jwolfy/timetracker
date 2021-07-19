<template>
  <div class="container single-task">
    <div class="task-delete-button">
      <b-button
        size="is-small is-text"
        icon-right="trash-alt"
        type="is-danger is-light"
        @click="deleteTask(task.id)"
      >
      </b-button>
    </div>
    <div class="task-edit-button">
      <b-button size="is-small is-text" icon-right="edit"> </b-button>
    </div>
    <div class="task-comment">
      {{ task.comment }}
    </div>
    <div class="task-duration">
      {{ secondsToHours(task.duration) }}
    </div>
    <div class="task-start-button">
      <b-button
        v-if="isTimerRunningForTask(task.id)"
        size="is-small is-text rounded"
        type="is-danger is-light"
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
import { secondsToHours } from "@/service/utils";
import { mapActions, mapGetters } from "vuex";

export default {
  props: { task: Object },
  computed: {
    ...mapGetters(["isTimerRunningForTask"]),
  },
  methods: {
    ...mapActions(["deleteTask", "startTimer", "stopTimer"]),
    secondsToHours: secondsToHours,
    removeTask(id) {
      this.deleteTask(id);
    },
    startTask(id) {
      this.startTimer(id);
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
}

.task-comment {
  flex: 15;
}

.task-duration {
  flex: 1;
}

.task-start-button {
  flex: 1;
}
</style>
