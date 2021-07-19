<template>
  <div>
    Timer
    {{ timer }}
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  methods: {
    ...mapActions(["fetchTimer"]),
  },
  computed: {
    ...mapGetters(["timer"]),
  },
  created() {
    this.fetchTimer();
  },
};
</script>
