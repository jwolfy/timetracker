const totalDurationForPeriod = (data) => {
  if ("tasks" in data) {
    return totalForSingleIssue(data.tasks).toFixed(1);
  } else {
    const firstKey = Object.keys(data)[0];
    if (Number.isInteger(Number(firstKey))) {
      return totalForOneDay(data).toFixed(1);
    } else {
      console.log(data)
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

export { totalDurationForPeriod };
