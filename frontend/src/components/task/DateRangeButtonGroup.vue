<template>
  <div class="container date-ranges">
    <b-button
      v-for="range in dateRanges"
      :key="range.name"
      type="is-ghost"
      @click="
        fetchTasks({ startDate: range.startDate, endDate: range.endDate })
      "
    >
      {{ range.name }}
    </b-button>
    <b-button type="is-ghost" @click="$refs.rangeDatepicker.toggle()">
      Custom range
    </b-button>
    <b-datepicker
      ref="rangeDatepicker"
      expanded
      range
      v-model="dates"
      :range-end="handleDateRange()"
    ></b-datepicker>
  </div>
</template>

<script>
import moment from "moment";
import { mapActions } from "vuex";
import { toDate } from "@/service/utils";

export default {
  data() {
    return {
      dateRanges: [
        {
          name: "Today",
          startDate: this.toDate(moment()),
          endDate: this.toDate(moment()),
        },
        {
          name: "Yesterday",
          startDate: this.toDate(moment().subtract(1, "days")),
          endDate: this.toDate(moment().subtract(1, "days")),
        },
        {
          name: "This week",
          startDate: this.toDate(moment().startOf("isoWeek")),
          endDate: this.toDate(moment()),
        },
        {
          name: "Last week",
          startDate: this.toDate(
            moment()
              .startOf("isoWeek")
              .subtract(7, "days")
          ),
          endDate: this.toDate(
            moment()
              .startOf("isoWeek")
              .subtract(1, "days")
          ),
        },
        {
          name: "This month",
          startDate: this.toDate(moment().startOf("month")),
          endDate: this.toDate(moment()),
        },
        {
          name: "Last month",
          startDate: this.toDate(
            moment()
              .startOf("month")
              .subtract(1, "month")
          ),
          endDate: this.toDate(
            moment()
              .startOf("month")
              .subtract(1, "days")
          ),
        },
      ],
      dates: [],
    };
  },
  methods: {
    ...mapActions(["fetchTasks"]),
    toDate: toDate,
    handleDateRange() {
      this.fetchTasks({
        startDate: this.toDate(moment(this.dates[0])),
        endDate: this.toDate(moment(this.dates[1])),
      });
      this.dates = [];
    },
  },
};
</script>

<style scoped>
.date-ranges {
  display: flex;
  justify-content: flex-start;
}
</style>
