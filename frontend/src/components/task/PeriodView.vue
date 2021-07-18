<template>
  <div class="container">
    <div class="total-for-period is-size-4 has-text-right">
      {{ totalForPeriod(groupedTasks) }}
    </div>
    <div v-for="(data, date) in groupedTasks" :key="date" class="mb-4">
      <DayView :date="date" :data="data" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DayView from "@/components/task/DayView";
import { totalDurationForPeriod } from "@/service/utils";

export default {
  name: "PeriodView",
  components: { DayView },
  computed: {
    ...mapGetters(["groupedTasks"]),
  },
  methods: {
    totalForPeriod: totalDurationForPeriod,
  },
};
</script>
