<template>
  <b-field grouped>
    <b-datepicker
      placeholder="Date"
      icon="calendar-today"
      editable
    ></b-datepicker>
    <b-autocomplete
      v-model="issue_id"
      placeholder="Issue"
      :keep-first="true"
      :open-on-focus="true"
      :clearable="true"
      :data="filteredIssues"
      field="issue_id"
      :custom-formatter="(issue) => `${issue.issue_id} - ${issue.subject}`"
    ></b-autocomplete>
    <b-input placeholder="Subject" v-model="subject"></b-input>
    <b-button type="is-success">Add</b-button>
  </b-field>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AddTaskForm",
  data() {
    return {
      issue_id: "",
      issue: {},
      spent_on: "",
      subject: "",
    };
  },
  computed: {
    ...mapGetters(["allIssues"]),
    filteredIssues() {
      return this.allIssues.filter((issue) => {
        return (
          issue.issue_id.toString().indexOf(this.issue_id) >= 0 ||
          issue.subject.toLowerCase().indexOf(this.issue_id.toLowerCase()) >= 0
        );
      });
    },
  },
};
</script>
