<template>
  <div>
    <section class="section">
      <AddTaskForm />
    </section>
    <section class="section">
      <PeriodView />
    </section>
  </div>
</template>

<script>
import AddTaskForm from "@/components/task/AddTaskForm";
import PeriodView from "@/components/task/PeriodView";

export default {
  name: "Tasks",
  components: {
    AddTaskForm,
    PeriodView,
  },
};
</script>
