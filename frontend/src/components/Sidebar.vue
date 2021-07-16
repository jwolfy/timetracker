<template>
  <aside class="sidebar">
    <div class="sidebar-menu"></div>
    <ul>
      <li><router-link to="/">Tasks</router-link></li>
      <li><router-link to="/issues">Issues</router-link></li>
      <li><router-link to="/settings">Settings</router-link></li>
      <li>
        <span v-if="isLoggedIn"><a @click="logout">Logout</a></span>
      </li>
    </ul>
  </aside>
</template>

<script>
export default {
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
  },
};
</script>
