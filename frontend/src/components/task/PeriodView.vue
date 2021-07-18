<template>
  <div class="container">
    {{ totalForPeriod(groupedTasks) }}
    <div v-for="(data, date) in groupedTasks" :key="date">
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
