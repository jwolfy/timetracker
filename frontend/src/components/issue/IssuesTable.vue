<template>
  <b-table
    :data="allIssues"
    striped
    narrowed
    paginated
    pagination-size="is-small"
    pagination-position="both"
    per-page="50"
  >
    <b-table-column
      field="issue_id"
      label="ID"
      width="100"
      sortable
      numeric
      v-slot="props"
      searchable
    >
      {{ props.row.issue_id }}
    </b-table-column>
    <b-table-column
      field="subject"
      label="Subject"
      sortable
      searchable
      v-slot="props"
    >
      {{ props.row.subject }}
    </b-table-column>
    <b-table-column field="is_active" label="Is active" sortable v-slot="props">
      <b-checkbox v-model="props.row.is_active" disabled> </b-checkbox>
    </b-table-column>
  </b-table>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  methods: {
    ...mapActions(["fetchIssues"]),
  },
  computed: {
    ...mapGetters(["allIssues"]),
  },
  created() {
    this.fetchIssues();
  },
};
</script>
