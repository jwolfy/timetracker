<template>
  <div>
    {{ date }}
    <div v-for="(data, issue_id) in data" :key="issue_id">
      {{ issue_id }}
      {{ data.issue }}
      {{ data.tasks }}
    </div>
  </div>
</template>

<script>
import { totalDurationForPeriod } from "@/service/utils";

export default {
  props: {
    date: String,
    data: Object,
  },
  methods: {
    totalForPeriod: totalDurationForPeriod,
  },
};
</script>
