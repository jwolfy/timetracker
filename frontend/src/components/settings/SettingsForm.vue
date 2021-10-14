<template>
  <section>
    <b-field horizontal label="Redmine URL">
      <template #label>
        Redmine URL
        <b-tooltip
          type="is-dark"
          label="Issue titles will become links to corresponding tickets based on this domain"
        >
          <b-icon size="is-small" icon="question-circle"></b-icon>
        </b-tooltip>
      </template>
      <b-input
        v-model="redmineUrl"
        placeholder="https://www.redmine.org"
      ></b-input>
    </b-field>
    <b-field horizontal>
      <p class="control">
        <b-button
          @click="updateSettings"
          label="Save"
          type="is-primary"
        ></b-button>
      </p>
    </b-field>
  </section>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      redmineUrl: "",
    };
  },
  methods: {
    ...mapActions(["fetchSettings", "saveSettings"]),
    updateSettings() {
      this.saveSettings({
        redmine_url: this.redmineUrl,
      });
    },
  },
  watch: {
    settings: function(settings) {
      this.redmineUrl = settings.redmine_url;
    },
  },
  created() {
    this.fetchSettings();
  },
  computed: {
    ...mapGetters(["settings"]),
  },
};
</script>
