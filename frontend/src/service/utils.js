import moment from "moment";
import { ToastProgrammatic as Toast } from "buefy";

const totalDurationForPeriod = (data) => {
  if ("tasks" in data) {
    return totalForSingleIssue(data.tasks).toFixed(1);
  } else {
    const firstKey = Object.keys(data)[0];
    if (Number.isInteger(Number(firstKey))) {
      return totalForOneDay(data).toFixed(1);
    } else {
      return totalForDays(data).toFixed(1);
    }
  }
};

const totalForSingleIssue = (tasks) => {
  var total = 0;
  tasks.forEach((task) => (total += secondsToHours(task.duration)));
  return total;
};

const totalForOneDay = (issuesData) => {
  var total = 0;
  Object.values(issuesData).forEach(
    (value) => (total += totalForSingleIssue(value.tasks))
  );
  return total;
};

const totalForDays = (daysData) => {
  var total = 0;
  Object.values(daysData).forEach((value) => (total += totalForOneDay(value)));
  return total;
};

const secondsToHours = (duration) => {
  return Math.round((duration / 3600) * 10) / 10;
};

const dateToString = (date) => {
  if (date instanceof Date) {
    return moment(date).format("YYYY-MM-DD");
  }
  return date.format("YYYY-MM-DD");
};

const stringToDate = (str) => {
  return moment(str, "YYYY-MM-DD").toDate();
};

const formatTime = (sec) => {
  let hours = Math.floor(sec / 3600)
    .toString()
    .padStart(2, "0");
  let minutes = Math.floor((sec - hours * 3600) / 60)
    .toString()
    .padStart(2, "0");
  let seconds = sec - (hours * 3600 + minutes * 60).toString().padStart(2, "0");

  var time = "";

  if (hours !== "00") {
    time += `${hours} : `;
  }

  time += `${minutes} : ${seconds}`;

  return time;
};

const toast = (text, type = "is-success") => {
  type = type === "error" ? "is-danger" : "is-success";
  Toast.open({
    message: text,
    type: type,
    position: "is-bottom-right",
  });
};

export {
  totalDurationForPeriod,
  secondsToHours,
  dateToString,
  formatTime,
  stringToDate,
  toast,
};
