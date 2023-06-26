







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
