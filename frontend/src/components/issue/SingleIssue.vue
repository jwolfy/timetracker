<template>
  <div class="container single-issue">
    <div class="issue-edit-button" @click="editIssueById(issue.issue_id)">
      <b-button size="is-small is-text" icon-right="edit"> </b-button>
    </div>
    <div class="issue-id">
      {{ issue.issue_id }}
    </div>
    <div class="issue-subject">
      {{ issue.subject }}
    </div>
    <div class="issue-is-active">
      <b-checkbox v-model="issue.is_active" disabled> </b-checkbox>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: { issue: Object },
  methods: {
    ...mapActions(["editIssue"]),
    editIssueById(id) {
      this.editIssue(id);
    },
  },
};
</script>

<style scoped>
.single-issue {
  display: flex;
}

.issue-edit-button {
  flex: 1;
  opacity: 0;
}

.issue-id {
  flex: 1;
}

.issue-subject {
  flex: 13;
}

.issue-is-active {
  flex: 1;
}

.single-issue:hover .issue-edit-button {
  opacity: 0.7;
}
</style>
