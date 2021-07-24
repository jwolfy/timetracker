<template>
  <div class="card mb-1 p-1">
    <div v-for="issue in allIssues" :key="issue.issue_id">
      <SingleIssueEdited :issue="issue" v-if="editedIssueId === issue.issue_id" />
      <SingleIssue :issue="issue" v-else/>
    </div>
  </div>
</template>

<script>
import SingleIssue from "@/components/issue/SingleIssue";
import SingleIssueEdited from "@/components/issue/SingleIssueEdited";
import { mapActions, mapGetters } from "vuex";

export default {
  components: { SingleIssue, SingleIssueEdited },
  methods: {
    ...mapActions(["fetchIssues"]),
    searchByIssueId(row, input) {
      return row.issue_id.toString().indexOf(input) >= 0;
    },
  },
  computed: {
    ...mapGetters(["allIssues", "editedIssueId"]),
  },
  created() {
    this.fetchIssues();
  },
};
</script>
