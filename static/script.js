console.log("hi");

// Access the data passed from the backend
let overallLabels = [];
let overallO2Levels = [];
let overallHeartRates = [];
let overallTemperatures = [];
let time_today = [];
let o2_today = [];
let heart_rates_today = [];
let temp_today = [];
let o2TodayChart = null;
// Create the charts

// Function to create all the charts
function createCharts(time_today) {
  const chartTypes = ["o2", "o2_today", "hr", "hr_today", "temp", "temp_today"];

  chartTypes.forEach((chartType) => {
    const chartContainer = document.getElementById(`${chartType}-chart`);
    createChart(chartType, chartContainer, time_today, heart_rates_today);
  });

  // ...
}

// Function to create a chart with the specified type
function createChart(chartType, container, time_today, heart_rates_today) {
  const data = [];
  let yData = [];

  if (chartType === "o2") {
    // Oxygen Levels
    yData = overallO2Levels;
    // console.log(overallLabels)
    data.push({
      x: overallLabels,
      y: yData,
      type: "scatter",
      line: { color: "rgba(75, 192, 192, 1)" },
      name: "Oxygen Levels ",
    });
    title = "O2 Levels";
    ytitle = "SpO2";
  } else if (chartType === "o2_today") {
    // Heart Rate
    // console.log(o2_today)
    yData = o2_today;
    // console.log(o2_today)
    data.push({
      x: time_today,
      y: yData,
      type: "scatter",
      line: { color: "rgba(75, 192, 192, 1)" },
      name: "O2 levels ",
    });
    title = "O2 levels today";
    ytitle = "SpO2";
    const layout = {
      title: title,
      xaxis: {
        title: "Time",
        type: "date",
        tickformat: "%H:%M", // Customize the tick format for time
      },
      yaxis: {
        title: ytitle,
      },
    };
    if (yData.length === 0) {
      layout.yaxis.range = [80, 100];
    }

    o2TodayChart = Plotly.plot(container, data, layout);
    return; // Exit the function after plotting the "o2_today" chart
  } else if (chartType === "hr") {
    // Heart Rate
    yData = overallHeartRates;
    data.push({
      x: overallLabels,
      y: yData,
      type: "scatter",
      line: { color: "rgba(255, 0, 0, 1)" },
      name: "Heart Rate levels ",
    });
    title = "Heart Rate Levels";
    ytitle = "Heart rate";
  } else if (chartType === "hr_today") {
    // Heart Rate
    yData = heart_rates_today;
    console.log(yData);
    data.push({
      x: time_today,
      y: yData,
      type: "scatter",
      line: { color: "rgba(255, 0, 0, 1)" },
      name: "Heart Rate levels ",
    });
    title = "Heart Rate Levels";
    ytitle = "Heart rate";
  } else if (chartType === "temp") {
    // Temperature
    yData = overallTemperatures;
    data.push({
      x: overallLabels,
      y: yData,
      type: "scatter",
      line: { color: "rgba(0, 0, 255, 1)" },
      name: "Temperature",
    });
    title = "Temperature";
    ytitle = "Fahrenheit";
  } else if (chartType === "temp_today") {
    // Temperature
    yData = temp_today;
    data.push({
      x: time_today,
      y: yData,
      type: "scatter",
      line: { color: "rgba(0, 0, 255, 1)" },
      name: "Temperature",
    });
    title = "Temperature";
    ytitle = "Fahrenheit";
  }

  const layout = {
    title: title,
    xaxis: {
      title: "Date",
      type: "date",
    },
    yaxis: {
      title: ytitle,
    },
  };
  if (yData.length === 0) {
    layout.yaxis.range = [80, 100];
  }

  Plotly.newPlot(container, data, layout);
}

// Update the charts
// Update the charts
// Update the charts
// Update the charts
function updateCharts(
    labels,
    o2Levels,
    heartRates,
    temperatures,
    o2_levels_today,
    heart_rates_today,
    temperature_today,
    time_today
  ) {
    overallLabels = labels;
    overallO2Levels = o2Levels;
    overallHeartRates = heartRates;
    overallTemperatures = temperatures;
    o2_today = o2_levels_today;
    heart_rates_today = heart_rates_today;
    time_today = time_today;
    temp_today = temperature_today;
    console.log(heart_rates_today);
  
    const chartContainers = document.querySelectorAll(".chart-container");
    chartContainers.forEach((container, index) => {
      const chartType = ["o2", "o2_today", "hr", "hr_today", "temp", "temp_today"][index];
      if (chartType === "o2_today") {
        // Update the "o2_today" chart using Plotly.extendTraces or Plotly.update
        const yData = o2_today;
        const numDataPoints = yData.length;
  
        if (numDataPoints > 0) {
          if (o2TodayChart) {
            // Chart already exists, extend the existing traces
            const lastDataPoint = { x: [[time_today[time_today.length - 1]]], y: [[yData[yData.length - 1]]] };
            Plotly.extendTraces(
              container,
              lastDataPoint,
              [0] // Trace index to extend
            );
          } else {
            // Chart doesn't exist, create it for the first time
            const data = [
              {
                x: [time_today],
                y: [yData],
                type: "scatter",
                line: { color: "rgba(75, 192, 192, 1)" },
                name: "O2 levels",
              },
            ];
  
            const layout = {
              title: "O2 levels today",
              xaxis: {
                title: "Time",
                type: "date",
                tickformat: "%H:%M:%S", // Customize the tick format for time
              },
              yaxis: {
                title: "SpO2",
              },
            };
  
            o2TodayChart = Plotly.newPlot(container, data, layout);
          }
        } else {
          // No data points available, update the range of y-axis
          if (o2TodayChart) {
            const updateLayout = {
              "yaxis.range": [80, 100],
            };
            Plotly.update(container, {}, updateLayout);
          }
        }
      } else {
        // Update other charts
        createChart(chartType, container, time_today, heart_rates_today);
      }
    });
  }
  
  

// Function to send a POST request to generate and save random data
function sendObservationData() {
  const urlParts = window.location.href.split("/");
  const patientId = urlParts[urlParts.length - 1];
  $.ajax({
    url: `/fhir/observation/${patientId}`,
    type: "POST",
    success: function (response) {
      console.log("Data generated and saved successfully");
    },
    error: function (xhr, status, error) {
      console.error("Error generating and saving data:", error);
    },
  });
}

// Function to send a GET request to retrieve the latest data for visualization
function getObservationData() {
  const urlParts = window.location.href.split("/");
  const patientId = urlParts[urlParts.length - 1];
  $.ajax({
    url: `/fhir/observation?id=${patientId}`,
    type: "GET",
    success: function (response) {
      const {
        timestamps,
        o2_levels,
        heart_rates,
        temperatures,
        o2_levels_today,
        heart_rates_today,
        temperature_today,
        time_today,
      } = response;
      // console.log(time_today);
      updateCharts(
        timestamps,
        o2_levels,
        heart_rates,
        temperatures,
        o2_levels_today,
        heart_rates_today,
        temperature_today,
        time_today
      );
      console.log(heart_rates_today);

      console.log("Data retrieved successfully");
    },
    error: function (xhr, status, error) {
      console.error("Error retrieving data:", error);
    },
  });
}

function sendAndRetrieveObservationData() {
//   sendObservationData();  // Call the function to send observation data
  getObservationData(); // Call the function to retrieve observation data
}

// Call the sendAndRetrieveObservationData function initially

// Example usage: Trigger the updateCharts() function when the container is loaded

// Helper function to group the data by day
// function groupByDay(labels, data) {
//     const groupedData = {};
//     for (let i = 0; i < labels.length; i++) {
//         const label = labels[i];
//         const value = data[i];
//         const day = label.substring(0, 10); // Extract the date part from the timestamp
//         if (!groupedData[day]) {
//             groupedData[day] = [];
//         }
//         groupedData[day].push(value);
//     }
//     return groupedData;
// }

// // Helper function to calculate the average of an array of numbers
// function calculateAverage(numbers) {
//     const sum = numbers.reduce((a, b) => a + b, 0);
//     return sum / numbers.length;
// }

// Calculate the overall trend by taking the average of vital signs for each day
// const overallLabels = [];
// const overallO2LevelsAvg = [];
// const overallHeartRatesAvg = [];

// // Group the vital signs by day
// const groupedByDayO2 = groupByDay(dayLabels, dayO2Levels);
// const groupedByDayHR = groupByDay(dayLabels, dayHeartRates);

// // Calculate the average oxygen level and heart rate for each day
// for (const [date, o2Levels] of Object.entries(groupedByDayO2)) {
//     const avgO2Level = calculateAverage(o2Levels);
//     overallLabels.push(date);
//     overallO2LevelsAvg.push(avgO2Level);
// }

// for (const [date, heartRates] of Object.entries(groupedByDayHR)) {
//     const avgHeartRate = calculateAverage(heartRates);
//     overallHeartRatesAvg.push(avgHeartRate);
// }
