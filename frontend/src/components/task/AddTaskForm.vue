<template>
  <b-field>
    <b-datepicker
      placeholder="Date"
      v-model="spent_on"
      icon="calendar-alt"
      editable
      :date-formatter="(date) => toDate(date)"
    ></b-datepicker>
    <b-autocomplete
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
      @keyup.native.enter="createTask"
      placeholder="Comment"
      v-model="comment"
    ></b-input>
    <b-button type="is-success" @click="createTask">Add</b-button>
  </b-field>
</template>

<script>
import moment from "moment";
import { mapGetters, mapActions } from "vuex";
import { toDate } from "@/service/utils";

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
    toDate: toDate,
    createTask() {
      if (this.comment === "") {
        return;
      }
      this.addTask({
        issue_id: this.selectedIssueId,
        spent_on: this.toDate(moment(this.spent_on)),
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
