<template>
  <section class="section">
    <div class="columns is-centered">
      <div class="column is-one-fifth">
        <b-field>
          <b-input placeholder="Name" v-model="username"></b-input>
        </b-field>
        <b-field>
          <b-input
            type="password"
            placeholder="Password"
            v-model="password"
            @keyup.native.enter="register"
          ></b-input>
        </b-field>
        <div class="field is-grouped is-grouped-centered">
          <div class="control">
            <button @click="register" class="button is-link">Register</button>
          </div>
        </div>
        <section class="section">
          <div class="columns is-centered">
            <a href="/login">Login</a>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    register: function() {
      let username = this.username;
      let password = this.password;
      this.$store
        .dispatch("register", { username, password })
        .then(() => this.$router.push("/login"))
        .catch((err) => console.log(err));
    },
  },
};
</script>