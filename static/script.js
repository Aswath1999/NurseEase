
// Access the data passed from the template
console.log(dayLabels);
console.log(dayO2Levels);
console.log(dayHeartRates);

// Rest of the JavaScript code goes here...


// Create the chart for the particular day
const dayChart = document.getElementById('dayChart');
const chartTypeSelect = document.getElementById('chartType');
let currentChartType = chartTypeSelect.value;
updateDayChart();

// Update both the day chart and the overall chart
function updateCharts() {
    currentChartType = chartTypeSelect.value;
    updateDayChart();
    updateOverallChart();
}

// Create the day chart with the specified type
function createDayChart(chartType) {
    const data = [];
    let yData = [];

    if (chartType === 'o2') {
        // Oxygen Levels
        yData = dayO2Levels;
        data.push({
            x: dayLabels,
            y: yData,
            type: 'scatter',
            line: { color: 'rgba(75, 192, 192, 1)' },
            name: 'Oxygen Levels',
        });
    } else if (chartType === 'hr') {
        // Heart Rate
        yData = dayHeartRates;
        data.push({
            x: dayLabels,
            y: yData,
            type: 'scatter',
            line: { color: 'rgba(255, 0, 0, 1)' },
            name: 'Heart Rate',
        });
    }

    const layout = {
        title: 'Day Chart',
        xaxis: {
            title: 'Time',
            type: 'date',
        },
        yaxis: {
            title: 'Value',
        },
    };

    Plotly.newPlot(dayChart, data, layout);
}

// Calculate the overall trend by taking the average of vital signs for each day
const overallLabels = [];
const overallO2LevelsAvg = [];
const overallHeartRatesAvg = [];

// Group the vital signs by day
const groupedByDayO2 = groupByDay(dayLabels, dayO2Levels);
const groupedByDayHR = groupByDay(dayLabels, dayHeartRates);

// Calculate the average oxygen level and heart rate for each day
for (const [date, o2Levels] of Object.entries(groupedByDayO2)) {
    const avgO2Level = calculateAverage(o2Levels);
    overallLabels.push(date);
    overallO2LevelsAvg.push(avgO2Level);
}

for (const [date, heartRates] of Object.entries(groupedByDayHR)) {
    const avgHeartRate = calculateAverage(heartRates);
    overallHeartRatesAvg.push(avgHeartRate);
}

// Create the overall chart for the specified type
const overallChart = document.getElementById('overallChart');
let currentChartTypeOverall = chartTypeSelect.value;
updateOverallChart();

// Create the day chart with the specified type
function createOverallChart(chartType) {
    const data = [];
    let yData = [];

    if (chartType === 'o2') {
        // Oxygen Levels
        yData = overallO2LevelsAvg;
        data.push({
            x: overallLabels,
            y: yData,
            type: 'scatter',
            line: { color: 'rgba(75, 192, 192, 1)' },
            name: 'Oxygen Levels',
        });
    } else if (chartType === 'hr') {
        // Heart Rate
        yData = overallHeartRatesAvg;
        data.push({
            x: overallLabels,
            y: yData,
            type: 'scatter',
            line: { color: 'rgba(255, 0, 0, 1)' },
            name: 'Heart Rate',
        });
    }

    const layout = {
        title: 'Overall Trend',
        xaxis: {
            title: 'Date',
            type: 'date',
        },
        yaxis: {
            title: 'Average Value',
        },
    };

    Plotly.react(overallChart, data, layout);
}

// Helper function to group the data by day
function groupByDay(labels, data) {
    const groupedData = {};
    for (let i = 0; i < labels.length; i++) {
        const label = labels[i];
        const value = data[i];
        const day = label.substring(0, 10); // Extract the date part from the timestamp
        if (!groupedData[day]) {
            groupedData[day] = [];
        }
        groupedData[day].push(value);
    }
    return groupedData;
}

// Helper function to calculate the average of an array of numbers
function calculateAverage(numbers) {
    const sum = numbers.reduce((a, b) => a + b, 0);
    return sum / numbers.length;
}

// Update the day chart based on the selected type
function updateDayChart() {
    createDayChart(currentChartType);
}

// Update the overall chart based on the selected type
function updateOverallChart() {
    createOverallChart(currentChartType);
}