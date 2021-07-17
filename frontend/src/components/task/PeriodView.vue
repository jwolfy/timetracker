<template>
  <div class="container">
    <h1 class="is-size-3">Period view</h1>
    {{ groupedTasks }}
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
