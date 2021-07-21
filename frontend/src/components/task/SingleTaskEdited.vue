<template>
  <div class="container single-edited-task">
    <div class="task-cancel-button">
      <b-button
        size="is-small is-text"
        icon-right="window-close"
        type="is-light"
        @click="cancelEditTask"
      >
      </b-button>
    </div>
    <div class="task-save-button">
      <b-button
        size="is-small is-text"
        icon-right="save"
        type="is-success is-light"
        @click="saveTask"
      >
      </b-button>
    </div>
    <div class="task-comment">
      <b-input
        @keyup.native.enter="saveTask"
        size="is-small"
        v-model="comment"
      ></b-input>
    </div>
    <div class="task-delete-button">
      <b-button
        size="is-small is-text"
        icon-right="trash-alt"
        type="is-danger is-light"
        @click="deleteTask(id)"
      >
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  data() {
    return {
      comment: "",
      id: null,
    };
  },
  computed: {
    ...mapGetters(["editedTask"]),
  },
  methods: {
    ...mapActions(["deleteTask", "cancelEditTask", "updateTask"]),
    saveTask() {
      this.updateTask(
        Object.assign({}, this.editedTask, { comment: this.comment })
      );
      this.cancelEditTask();
    },
  },
  created() {
    this.id = this.editedTask.id;
    this.comment = this.editedTask.comment;
  },
};
</script>

<style scoped>
.single-edited-task {
  display: flex;
  align-items: center;
}

.task-save-button {
  flex: 1;
}

.task-cancel-button {
  flex: 1;
}

.task-comment {
  flex: 15;
}

.task-delete-button {
  flex: 1;
}
</style>
