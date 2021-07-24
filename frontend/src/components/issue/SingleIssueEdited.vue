<template>
  <div class="container single-edited-issue">
    <div class="issue-cancel-button">
      <b-button
        size="is-small is-text"
        icon-right="window-close"
        type="is-light"
        @click="cancelEditIssue"
      >
      </b-button>
    </div>
    <div class="issue-save-button">
      <b-button
        size="is-small is-text"
        icon-right="save"
        type="is-success is-light"
        @click="saveIssue"
      >
      </b-button>
    </div>
    <div class="issue-subject">
      <b-input
        @keyup.native.enter="saveIssue"
        size="is-small"
        v-model="subject"
      ></b-input>
    </div>
    <div class="issue-is-active">
      <b-checkbox v-model="is_active"> </b-checkbox>
    </div>
    <div class="issue-delete-button">
      <b-button
        size="is-small is-text"
        icon-right="trash-alt"
        type="is-danger is-light"
        @click="deleteIssue(id)"
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
      subject: "",
      is_active: null,
    };
  },
  computed: {
    ...mapGetters(["editedIssue"]),
  },
  methods: {
    ...mapActions(["cancelEditIssue", "deleteIssue", "updateIssue"]),
    saveIssue() {
      this.updateIssue(
        Object.assign({}, this.editedIssue, {
          subject: this.subject,
          is_active: this.is_active,
        })
      );
      this.cancelEditIssue();
    },
  },
  created() {
    this.id = this.editedIssue.issue_id;
    this.subject = this.editedIssue.subject;
    this.is_active = this.editedIssue.is_active;
  },
};
</script>

<style scoped>
.single-edited-issue {
  display: flex;
  align-items: center;
}

.issue-save-button {
  flex: 1;
}

.issue-cancel-button {
  flex: 1;
}

.issue-subject {
  flex: 15;
}

.issue-is-active {
  flex: 1;
}

.issue-delete-button {
  flex: 1;
}
</style>
