<template>
  <div class="card mb-1 p-1">
    <div class="issue-name-with-total has-text-weight-semibold mb-1">
      <div class="issue-name">
        {{ `${data.issue.issue_id} - ${data.issue.subject}` }}
      </div>
      <div class="total-for-issue">
        {{ totalForPeriod(data) }}
      </div>
    </div>
    <div v-for="task in data.tasks" :key="task.id">
      <SingleTask :task="task" />
    </div>
  </div>
</template>

<script>
import SingleTask from "@/components/task/SingleTask";
import { totalDurationForPeriod } from "@/service/utils";

export default {
  components: { SingleTask },
  props: { data: Object },
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
  flex: 6
}

.total-for-issue {
  flex: 1;
}
</style>
