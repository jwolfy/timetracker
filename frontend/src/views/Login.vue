<template>
  <section class="section">
    <div class="columns is-centered">
      <div class="column is-one-fifth">
        <b-field>
          <b-input placeholder="Name" v-model="name"></b-input>
        </b-field>
        <b-field>
          <b-input
            type="password"
            placeholder="Password"
            v-model="password"
            @keyup.native.enter="login"
          ></b-input>
        </b-field>
        <div class="field is-grouped is-grouped-centered">
          <div class="control">
            <button @click="login" class="button is-link">Login</button>
          </div>
        </div>
        <section class="section">
          <div class="columns is-centered">
            <a href="/register">Create new account</a>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      name: "",
      password: "",
    };
  },
  methods: {
    login: function() {
      let name = this.name;
      let password = this.password;
      this.$store
        .dispatch("login", { name, password })
        .then(() => this.$router.push("/"))
        .catch((err) => console.log(err));
    },
  },
};
</script>
