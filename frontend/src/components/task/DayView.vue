<template>
  <div>
    <div class="container day-title">
      <div class="date is-size-4 has-text-grey">
        {{ date }}
      </div>
      <div class="total-for-day is-size-5 has-text-right">
        {{ totalForPeriod(data) }}
      </div>
    </div>
    <div v-for="(issueData, issue_id) in data" :key="issue_id">
      <IssueView :data="issueData" />
    </div>
  </div>
</template>

<script>
import { totalDurationForPeriod } from "@/service/utils";
import IssueView from "@/components/task/IssueView";

export default {
  components: { IssueView },
  props: {
    date: String,
    data: Object,
  },
  methods: {
    totalForPeriod: totalDurationForPeriod,
  },
};
</script>

<style scoped>
.day-title {
  display: flex;
  align-items: center;
}

.date {
  flex: 1
}

.total-for-day {
  flex: 1;
}
</style>
