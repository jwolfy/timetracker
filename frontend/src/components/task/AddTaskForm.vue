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
      name: "",
      selectedIssueId: null,
      spent_on: new Date(),
      subject: "",
    };
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
};
</script>
