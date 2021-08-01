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
        first-day-of-week="1"
        icon="calendar-alt"
        :date-formatter="(date) => dateToString(date)"
        size="is-small"
      ></b-datepicker>
    </div>
    <div class="task-issue-id">
      <b-autocomplete
        icon="search"
        size="is-small"
        v-model="issueName"
        placeholder="Issue"
        open-on-focus
        :keep-first="true"
        :clearable="true"
        :data="filteredIssues"
        field="issue_id"
        :custom-formatter="(issue) => `${issue.issue_id} - ${issue.subject}`"
        @select="
          (option) => (issueId = option != null ? option.issue_id : null)
        "
      ></b-autocomplete>
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
      issueId: null,
      comment: "",
      spentOn: null,
      durationHours: 0,
      issueName: "",
    };
  },
  computed: {
    ...mapGetters(["editedTask", "allIssues", "issueById"]),
    filteredIssues() {
      return this.allIssues.filter((issue) => {
        return (
          issue.issue_id.toString().indexOf(this.issueName) >= 0 ||
          issue.subject.toLowerCase().indexOf(this.issueName.toLowerCase()) >= 0
        );
      });
    },
  },
  methods: {
    ...mapActions(["deleteTask", "cancelEditTask", "updateTask"]),
    saveTask() {
      const seconds = parseInt(this.durationHours * 3600);
      this.updateTask(
        Object.assign({}, this.editedTask, {
          issue_id: this.issueId,
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
    this.issueId = this.editedTask.issue_id;
    this.comment = this.editedTask.comment;
    this.spentOn = this.stringToDate(this.editedTask.spent_on);
    this.durationHours = this.secondsToHours(this.editedTask.duration);

    const issue = this.issueById(this.editedTask.issue_id);
    this.issueName = `${issue.issue_id} - ${issue.subject}`;
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
  flex: 10;
}

.task-spent-on {
  flex: 4;
}

.task-issue-id {
  flex: 9;
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
