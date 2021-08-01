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
    <div class="task-spent-on">
      <b-datepicker
        placeholder="Date"
        v-model="spentOn"
        icon="calendar-alt"
        :date-formatter="(date) => dateToString(date)"
        size=is-small
      ></b-datepicker>
    </div>
    <div class="task-duration-formatted">
      {{ formatSecondsToTime(editedTask.duration) }}
    </div>
    <div class="task-duration-input">
      <b-input v-model="durationHours" type="number" size="is-small" step="0.1">
      </b-input>
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
import {
  formatTime,
  secondsToHours,
  stringToDate,
  dateToString,
} from "@/service/utils";

export default {
  data() {
    return {
      id: null,
      comment: "",
      spentOn: null,
      durationHours: 0,
    };
  },
  computed: {
    ...mapGetters(["editedTask"]),
  },
  methods: {
    ...mapActions(["deleteTask", "cancelEditTask", "updateTask"]),
    saveTask() {
      const seconds = parseInt(this.durationHours * 3600);
      this.updateTask(
        Object.assign({}, this.editedTask, {
          comment: this.comment,
          spent_on: this.dateToString(this.spentOn),
          duration: seconds,
        })
      );
      this.cancelEditTask();
    },
    formatSecondsToTime: formatTime,
    secondsToHours: secondsToHours,
    dateToString: dateToString,
    stringToDate: stringToDate,
  },
  created() {
    this.id = this.editedTask.id;
    this.comment = this.editedTask.comment;
    this.spentOn = this.stringToDate(this.editedTask.spent_on);
    this.durationHours = this.secondsToHours(this.editedTask.duration);
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

.task-spent-on {
  flex: 3;
}

.task-duration-formatted {
  flex: 3;
}

.task-duration-input {
  flex: 2;
}

.task-delete-button {
  flex: 1;
}
</style>
