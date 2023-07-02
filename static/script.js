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
let hrTodayChart = null;
let  tempTodayChart=null;
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
      mode: 'lines+markers',
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
        tickformat: "%H:%M:%S", // Customize the tick format for time
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
      mode: 'lines+markers',
      type: "scatter",
      line: { color: "rgba(255, 0, 0, 1)" },
      name: "Heart Rate levels ",
    });
    title = "HR levels today";
    ytitle = "Heart rate";
    const layout = {
      title: title,
      xaxis: {
        title: "Time",
        type: "date",
        tickformat: "%H:%M:%S", // Customize the tick format for time
      },
      yaxis: {
        title: ytitle,
      },
    };
    if (yData.length === 0) {
      layout.yaxis.range = [80, 100];
    }

    hrTodayChart = Plotly.plot(container, data, layout);
    return;
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
    ytitle = "Celcius";
  } else if (chartType === "temp_today") {
    // Temperature
    yData = temp_today;
    data.push({
      x: time_today,
      y: yData,
      mode: 'lines+markers',
      type: "scatter",
      line: { color: "rgba(0, 0, 255, 1)" },
      name: "Temperature",
    });
    title = "HR levels today";
    ytitle = "Heart rate";
    const layout = {
      title: title,
      xaxis: {
        title: "Time",
        type: "date",
        tickformat: "%H:%M:%S", // Customize the tick format for time
      },
      yaxis: {
        title: ytitle,
      },
    };
    if (yData.length === 0) {
      layout.yaxis.range = [80, 100];
    }

    tempTodayChart = Plotly.plot(container, data, layout);
    return;
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
  
    const chartContainers = document.querySelectorAll(".chart-container");
    chartContainers.forEach((container, index) => {
      const chartType = ["o2_today","o2","hr_today",  "hr",  "temp_today", "temp"][index];
  
      if (chartType === "o2_today") {
        // Update the "o2_today" chart using Plotly.extendTraces or Plotly.update
        const yData = o2_today;
        const numDataPoints = yData.length;
  
        if (numDataPoints > 0) {
          if (o2TodayChart) {
            // Chart already exists, extend the existing trace
            const lastDataPoints = {
              x: [time_today.slice(-1)], // Use only the last data point for x-axis
              y: [yData.slice(-1)], // Use only the last data point for y-axis
            };
            Plotly.extendTraces(container, lastDataPoints, [0]); // Extend the trace with new data points
          } else {
            // Chart doesn't exist, create it for the first time
            const data = [
              {
                x: time_today,
                y: yData,
                type: "scatter",
                mode: "lines+markers",
                line: { color: "rgba(75, 192, 192, 1)" },
                name: "O2 levels",
              },
            ];
            const lastTimestamp = time_today[numDataPoints - 1];
            const rangeEnd = new Date(lastTimestamp);
            rangeEnd.setMinutes(rangeEnd.getMinutes() + 2); // Add 2 minutes
            const range = [time_today[Math.max(0, numDataPoints - 10)], rangeEnd];
            const layout = {
              title: "O2 levels today",
              xaxis: {
                title: "Time",
                type: "date",
                tickformat: "%H:%M:%S", // Customize the tick format for time
                range: range,
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
      } else if (chartType === "hr_today") {
        // Update the "hr_today" chart using Plotly.extendTraces or Plotly.update
        const yData = heart_rates_today;
        const numDataPoints = yData.length;
  
        if (numDataPoints > 0) {
          if (hrTodayChart) {
            // Chart already exists, extend the existing trace
            const lastDataPoints = {
              x: [time_today.slice(-1)], // Use only the last data point for x-axis
              y: [yData.slice(-1)], // Use only the last data point for y-axis
            };
            Plotly.extendTraces(container, lastDataPoints, [0]); // Extend the trace with new data points
          } else {
            // Chart doesn't exist, create it for the first time
            const data = [
              {
                x: time_today,
                y: yData,
                type: "scatter",
                mode: "lines+markers",
                line: { color: "rgba(255, 0, 0, 1)" },
                name: "Heart Rate levels",
              },
            ];
            const lastTimestamp = time_today[numDataPoints - 1];
            const rangeEnd = new Date(lastTimestamp);
            rangeEnd.setMinutes(rangeEnd.getMinutes() + 2); // Add 2 minutes
            const range = [time_today[Math.max(0, numDataPoints - 10)], rangeEnd];
            const layout = {
              title: "Heart Rate Levels today",
              xaxis: {
                title: "Time",
                type: "date",
                tickformat:"%H:%M:%S", // Customize the tick format for time
                range: range,
              },
              yaxis: {
                title: "Heart rate",
              },
            };
  
            hrTodayChart = Plotly.newPlot(container, data, layout);
          }
        } else {
          // No data points available, update the range of y-axis
          if (hrTodayChart) {
            const updateLayout = {
              "yaxis.range": [60, 120],
            };
            Plotly.update(container, {}, updateLayout);
          }
        }
      } else if (chartType === "temp_today") {
        // Update the "temp_today" chart using Plotly.extendTraces or Plotly.update
        const yData = temp_today;
        const numDataPoints = yData.length;
  
        if (numDataPoints > 0) {
          if (tempTodayChart) {
            // Chart already exists, extend the existing trace
            const lastDataPoints = {
              x: [time_today.slice(-1)], // Use only the last data point for x-axis
              y: [yData.slice(-1)], // Use only the last data point for y-axis
            };
            Plotly.extendTraces(container, lastDataPoints, [0]); // Extend the trace with new data points
          } else {
            // Chart doesn't exist, create it for the first time
            const data = [
              {
                x: time_today,
                y: yData,
                mode: 'lines+markers',
                type: "scatter",
                line: { color: "rgba(0, 0, 255, 1)" },
                name: "Temperature",
              },
            ];
            const lastTimestamp = time_today[numDataPoints - 1];
            const rangeEnd = new Date(lastTimestamp);
            rangeEnd.setMinutes(rangeEnd.getMinutes() + 2); // Add 2 minutes
            const range = [time_today[Math.max(0, numDataPoints - 10)], rangeEnd];
            const layout = {
              title: "Temperature today",
              xaxis: {
                title: "Time",
                type: "date",
                tickformat: "%H:%M:%S", // Customize the tick format for time
                range: range,
              },
              yaxis: {
                title: "Celcius",
              },
            };
  
            tempTodayChart = Plotly.newPlot(container, data, layout);
          }
        } else {
          // No data points available, update the range of y-axis
          if (tempTodayChart) {
            const updateLayout = {
              "yaxis.range": [30, 40],
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
  sendObservationData();  // Call the function to send observation data
  getObservationData(); // Call the function to retrieve observation data
}

 // JavaScript code to handle the click event of the "BACK" button
 var backButton = document.querySelector('.back-button');
 backButton.addEventListener('click', function() {
     window.location.href = "/";
 });

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}