<template>
  <div id="app">
    <main>
      <section class="section">
        <component :is="layout">
          <router-view />
        </component>
      </section>
    </main>
  </div>
</template>

<script>
import MainLayout from "@/layouts/MainLayout";
import EmptyLayout from "@/layouts/EmptyLayout";
import { mapActions } from "vuex";

export default {
  name: "App",
  components: { MainLayout, EmptyLayout },
  computed: {
    layout() {
      return (this.$route.meta.layout || "empty") + "-layout";
    },
  },
  methods: {
    ...mapActions(["fetchSettings", "saveSettings"]),
  },
  created() {
    this.fetchSettings();
  },
};
</script>

<style>
html {
  height: 100%;
}
body {
  background-color: hsl(0, 0%, 96%);
  min-height: 100%;
}
</style>
