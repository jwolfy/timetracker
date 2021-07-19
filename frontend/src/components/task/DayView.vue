<template>
  <div>
    <div class="date is-size-4 has-text-grey">
      {{ date }}
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
