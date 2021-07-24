<template>
  <b-field>
    <b-input v-model="issueId" placeholder="ID"> </b-input>
    <b-input v-model="subject" placeholder="Subject"></b-input>
    <b-checkbox v-model="isActive">Is active</b-checkbox>
    <b-button type="is-success" @click="createIssue">Add</b-button>
  </b-field>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      issueId: null,
      subject: "",
      isActive: true,
    };
  },
  methods: {
    ...mapActions(["addIssue"]),
    createIssue() {
      if (this.subject === "") {
        return;
      }
      this.addIssue({
        issue_id: this.issueId,
        subject: this.subject,
        is_active: this.isActive,
      });
      this.issueId = null;
      this.subject = "";
    },
  },
};
</script>
