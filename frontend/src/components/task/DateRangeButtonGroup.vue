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
    <b-dropdown can-close append-to-body trap-focus position="is-bottom-left">
      <template #trigger>
        <b-button type="is-ghost">
          Custom dates
        </b-button>
      </template>
      <b-dropdown-item custom paddingless>
        <b-datepicker inline range v-model="customDates"> </b-datepicker>
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>

<script>
import moment from "moment";
import { mapActions } from "vuex";
import { dateToString } from "@/service/utils";

export default {
  data() {
    return {
      dateRanges: [
        {
          name: "Today",
          startDate: this.dateToString(moment()),
          endDate: this.dateToString(moment()),
        },
        {
          name: "Yesterday",
          startDate: this.dateToString(moment().subtract(1, "days")),
          endDate: this.dateToString(moment().subtract(1, "days")),
        },
        {
          name: "This week",
          startDate: this.dateToString(moment().startOf("isoWeek")),
          endDate: this.dateToString(moment()),
        },
        {
          name: "Last week",
          startDate: this.dateToString(
            moment()
              .startOf("isoWeek")
              .subtract(7, "days")
          ),
          endDate: this.dateToString(
            moment()
              .startOf("isoWeek")
              .subtract(1, "days")
          ),
        },
        {
          name: "This month",
          startDate: this.dateToString(moment().startOf("month")),
          endDate: this.dateToString(moment()),
        },
        {
          name: "Last month",
          startDate: this.dateToString(
            moment()
              .startOf("month")
              .subtract(1, "month")
          ),
          endDate: this.dateToString(
            moment()
              .startOf("month")
              .subtract(1, "days")
          ),
        },
      ],
      customDates: [],
    };
  },
  methods: {
    ...mapActions(["fetchTasks"]),
    dateToString: dateToString,
    handleDateRange() {
      this.fetchTasks({
        startDate: this.dateToString(moment(this.dates[0])),
        endDate: this.dateToString(moment(this.dates[1])),
      });
      this.dates = [];
    },
  },
  watch: {
    customDates: function() {
      this.fetchTasks({
        startDate: this.dateToString(moment(this.customDates[0])),
        endDate: this.dateToString(moment(this.customDates[1])),
      });
      this.dates = [];
    },
  },
  created() {
    this.fetchTasks({startDate: this.dateToString(moment()), endDate: this.dateToString(moment())});
  }
};
</script>

<style scoped>
.date-ranges {
  display: flex;
  justify-content: flex-start;
}
</style>
