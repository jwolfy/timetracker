<template>
    <b-field grouped >
      <b-datepicker
        placeholder="Date"
        icon="calendar-today"
        editable
      ></b-datepicker>
      <b-input placeholder="Subject" v-model="subject"></b-input>
      <b-button type="is-success">Add</b-button>
    </b-field>
</template>

<script>
export default {
  name: "AddTaskForm",
  data() {
    return {
      spent_on: "",
      subject: "",
    };
  },
};
</script>
