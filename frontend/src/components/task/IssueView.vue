<template>
  <div class="card mb-1 p-1">
    <div class="issue-name-with-total has-text-weight-semibold mb-1">
      <div class="issue-name">
        <a
          v-if="redmine_url !== ''"
          v-bind:href="redmine_url + data.issue.issue_id"
          target="_blank"
        >
          {{ `${data.issue.issue_id} - ${data.issue.subject}` }}
        </a>
        <div v-else>{{ `${data.issue.issue_id} - ${data.issue.subject}` }}</div>
      </div>
      <div class="total-for-issue">
        {{ totalForPeriod(data) }}
      </div>
    </div>
    <div v-for="task in data.tasks" :key="task.id">
      <SingleTaskEdited :task="task" v-if="editedTaskId === task.id" />
      <SingleTask :task="task" v-else />
    </div>
  </div>
</template>

<script>
import SingleTask from "@/components/task/SingleTask";
import SingleTaskEdited from "@/components/task/SingleTaskEdited";
import { totalDurationForPeriod } from "@/service/utils";
import { mapGetters } from "vuex";

export default {
  components: { SingleTask, SingleTaskEdited },
  props: { data: Object },
  computed: {
    ...mapGetters(["editedTaskId", "redmine_url"]),
  },
  methods: {
    totalForPeriod: totalDurationForPeriod,
  },
};
</script>

<style scoped>
.issue-name-with-total {
  display: flex;
}

.issue-name {
  flex: 6;
}

.total-for-issue {
  flex: 1;
}

a {
  color: black;
}
</style>
