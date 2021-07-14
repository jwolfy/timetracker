<template>
  <div class="container main-layout">
    <Sidebar />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";

export default {
  name: "MainLayout",
  components: {
    Sidebar,
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
</style>
