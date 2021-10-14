<template>
  <b-field>
    <b-datepicker
      placeholder="Date"
      v-model="spent_on"
      :first-day-of-week="1"
      icon="calendar-alt"
      :date-formatter="(date) => dateToString(date)"
    ></b-datepicker>
    <b-autocomplete
      expanded
      icon="search"
      v-model="name"
      placeholder="Issue"
      :keep-first="true"
      :clearable="true"
      :data="filteredIssues"
      field="issue_id"
      :custom-formatter="(issue) => `${issue.issue_id} - ${issue.subject}`"
      @select="
        (option) => (selectedIssueId = option != null ? option.issue_id : null)
      "
    ></b-autocomplete>
    <b-input
      expanded
      @keyup.native.enter="createTask"
      placeholder="Comment"
      v-model="comment"
    ></b-input>
    <b-button type="is-primary" @click="createTask">Add</b-button>
  </b-field>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { dateToString } from "@/service/utils";

export default {
  name: "AddTaskForm",
  data() {
    return {
      name: "",
      selectedIssueId: null,
      spent_on: new Date(),
      comment: "",
    };
  },
  methods: {
    ...mapActions(["fetchIssues", "addTask"]),
    dateToString: dateToString,
    createTask() {
      if (this.comment === "") {
        return;
      }
      this.addTask({
        issue_id: this.selectedIssueId,
        spent_on: this.dateToString(this.spent_on),
        comment: this.comment,
      });
      this.comment = "";
    },
  },
  computed: {
    ...mapGetters(["allIssues"]),
    filteredIssues() {
      return this.allIssues.filter((issue) => {
        return (
          issue.issue_id.toString().indexOf(this.name) >= 0 ||
          issue.subject.toLowerCase().indexOf(this.name.toLowerCase()) >= 0
        );
      });
    },
  },
  created() {
    this.fetchIssues();
  },
};
</script>
