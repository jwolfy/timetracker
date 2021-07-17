<template>
  <div class="container">
    <h1 class="is-size-3">Period view</h1>
    <div v-for="(data, date) in groupedTasks" :key="date">
      {{ date }}
      {{ data }}
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "PeriodView",
  props: {
    data: Object,
  },
  methods: {},
  computed: {
    ...mapGetters(["groupedTasks"]),
  },
};
</script>
