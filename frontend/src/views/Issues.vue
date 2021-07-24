<template>
  <div>
    <AddIssueForm />
    <IssuesTable />
  </div>
</template>

<script>
import IssuesTable from "@/components/issue/IssuesTable";
import AddIssueForm from "@/components/issue/AddIssueForm";

export default {
  components: {
    IssuesTable,
    AddIssueForm,
  },
};
</script>
