<template>
  <div class="container main-layout">
    <Sidebar />
    <div class="main-content">
      <router-view />
    </div>
    <div class="timer">
      <Timer />
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Timer from "@/components/Timer";
import { mapActions } from "vuex";

export default {
  name: "MainLayout",
  components: {
    Sidebar,
    Timer,
  },
  methods: {
    ...mapActions(["fetchSettings"]),
  },
  created() {
    this.fetchSettings();
  },
};
</script>

<style scoped>
.main-layout {
  display: flex;
}

.sidebar {
  flex: 1;
}

.main-content {
  flex: 4;
}

.timer {
  flex: 1;
}
</style>
