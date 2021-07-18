<template>
  <div class="container single-task">
    <div class="task-delete-button">
      <b-button
        size="is-small is-text"
        icon-right="fas fa-trash-alt"
        type="is-danger is-light"
        @click="deleteTask(task.id)"
      >
      </b-button>
    </div>
    <div class="task-edit-button">
      <b-button size="is-small is-text" icon-right="fas fa-edit"> </b-button>
    </div>
    <div class="task-comment">
      {{ task.comment }}
    </div>
    <div class="task-duration">
      {{ secondsToHours(task.duration) }}
    </div>
    <div class="task-start-button">
      <b-button
        size="is-small is-text rounded"
        type="is-success is-light"
        icon-right="fas fa-play"
      ></b-button>
    </div>
  </div>
</template>

<script>
import { secondsToHours } from "@/service/utils";
import { mapActions } from "vuex";

export default {
  props: { task: Object },
  methods: {
    ...mapActions(["deleteTask"]),
    secondsToHours: secondsToHours,
    removeTask(id) {
      this.deleteTask(id);
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
