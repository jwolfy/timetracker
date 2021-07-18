const totalDurationForPeriod = (data) => {
  if ("tasks" in data) {
    console.log("single issue");
    console.log(data);
    return totalForSingleIssue(data.tasks).toFixed(1);
  } else {
    const firstKey = Object.keys(data)[0];
    console.log("firstKey: " + firstKey);
    if (Number.isInteger(Number(firstKey))) {
      console.log("one day");
      return totalForOneDay(data).toFixed(1);
    } else {
      console.log("days");
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
  console.log(daysData);
  Object.values(daysData).forEach((value) => (total += totalForOneDay(value)));
  return total;
};

const secondsToHours = (duration) => {
  return Math.round((duration / 3600) * 10) / 10;
};

export { totalDurationForPeriod };
