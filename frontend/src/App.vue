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

export default {
  name: "App",
  components: { MainLayout, EmptyLayout },
  computed: {
    layout() {
      return (this.$route.meta.layout || "empty") + "-layout";
    },
  },
  created: function() {
    this.$http.interceptors.response.use(undefined, function(err) {
      return new Promise(function() {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch("logout");
        }
        throw err;
      });
    });
  },
};
</script>

<style>
body {
  background: hsl(0, 0%, 96%);
  height: 100vh;
}
</style>
