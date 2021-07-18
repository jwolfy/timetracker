<template>
  <b-field>
    <b-datepicker
      placeholder="Date"
      v-model="spent_on"
      icon="calendar-alt"
      editable
      :date-formatter="(date) => date.toISOString().split('T')[0]"
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
      @select="(option) => (selectedIssueId = option.issue_id)"
    ></b-autocomplete>
    <b-input placeholder="Comment" v-model="comment"></b-input>
    <b-button type="is-success" @click="createTask">Add</b-button>
  </b-field>
</template>

<script>
import moment from "moment";
import { mapGetters, mapActions } from "vuex";
import { momentToDateString } from "@/service/utils";

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
    toDate(momentDate) {
      return momentToDateString(momentDate);
    },
    createTask() {
      console.log("add");
      const task = {
        issue_id: this.selectedIssueId,
        spent_on: this.toDate(moment(this.spent_on)),
        comment: this.comment,
      };
      this.comment = "";
      console.log(task);
      this.addTask(task);
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
