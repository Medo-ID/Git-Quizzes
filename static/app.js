// Burger menus
document.addEventListener('DOMContentLoaded', function() {
    // open
    const burger = document.querySelectorAll('.navbar-burger');
    const menu = document.querySelectorAll('.navbar-menu');

    if (burger.length && menu.length) {
        for (var i = 0; i < burger.length; i++) {
            burger[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }

    // close
    const close = document.querySelectorAll('.navbar-close');
    const backdrop = document.querySelectorAll('.navbar-backdrop');

    if (close.length) {
        for (var i = 0; i < close.length; i++) {
            close[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }

    if (backdrop.length) {
        for (var i = 0; i < backdrop.length; i++) {
            backdrop[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }
});

// get user history data
const jsonData = document.getElementById('data').dataset.json;

// Parse the JSON data
const appData = JSON.parse(jsonData);

// Function to count unique timestamps and create an object
function countUniqueTimestamps(dataArray) {
    // Create an object to store timestamp counts
    const timestampCounts = {};
  
    // Iterate through the array
    dataArray.forEach(item => {
      const timestamp = item.timestamp.split(' ')[0];
  
      // If the timestamp is not in the object, initialize its count to 1, otherwise increment
      timestampCounts[timestamp] = (timestampCounts[timestamp] || 0) + 1;
    });
  
    return timestampCounts;
}
  
// execute function for the testing
const timestampCounts = countUniqueTimestamps(appData);

// chart config
// date settings
function isoDaysOfWeek(dt) {
    let weekdays = dt.getDay(); // 0 to 6, where 0 is Sunday
    weekdays = (weekdays + 7) % 7 + 1; // 1 to 7 starting from Sunday
    return '' + weekdays;
}

// setup date: 365 days/squares and check if the user has some task in these days
function generateDays() {
    const day = new Date();
    const today = new Date(day.getFullYear(), day.getMonth(), day.getDate(),0, 0, 0, 0);
    const data_user = [];
    
    let dt = new Date(new Date().setDate(today.getDate() - 365));

    while (dt <= today) {
        const iso = dt.toISOString().substr(0, 10);
        const countForDate = timestampCounts[iso] || 0;

        data_user.push({
            x: iso,
            y: isoDaysOfWeek(dt),
            d: iso,
            v: countForDate
        });

        dt.setDate(dt.getDate() + 1);
    }

    console.log(data_user);
    return data_user;
}

// setup blocks
const data = {
    datasets: [{
        label: 'Track your daily activities',
        data: generateDays(),
        backgroundColor(d){
            const value = d.dataset.data[d.dataIndex].v;
            if (value == 0){
                return 'rgb(234, 234, 234)';
            } else if (value == 1 || value == 2){
                return 'rgb(238, 108, 77, 0.3)'
            } else if (value == 3 || value == 4){
                return 'rgb(238, 108, 77, 0.6)'
            }else if (value == 5 || value == 6){
                return 'rgb(238, 108, 77, 0.9)'
            }else {
                return 'rgb(238, 108, 77, 1)'
            }
        },
        borderColor: 'rgb(80, 80, 80)',
        borderRadius: 2,
        borderWidth: 1,
        hoverBackgroundColor: 'rgb(252, 225, 199)',
        hoverBorderColor: 'rgb(252, 225, 199)',
        width(w){
            const a = w.chart.chartArea || {};
            return (a.right - a.left) / 53 - 1;
        },
        height(h){
            const a = h.chart.chartArea || {};
            return (a.bottom - a.top) / 7 - 1;
        },
    }]
};

// scales block
const scales = {
    y: {
        type: 'time',
        offset: true,
        time: {
            unit: 'day',
            round: 'day',
            isoWeek: 1,
            parser: 'i',
            displayFormats: {
                day: 'iii'
            }
        },
        reverse: true,
        position: 'left',
        ticks: {
            maxRotation: 0,
            autoSkip: true,
            padding: 1,
            font: {
                size: 9
            }
        },
        grid: {
            display: false,
            drawBorder: false,
            tickLength: 0
        }
    },
    x: {
        type: 'time',
        position: 'top',
        offset: true,
        time: {
            unit: 'week',
            round: 'week',
            isoWeekDay: 0,
            displayFormats: {
                week: 'MMM'
            }
        },
        ticks: {
            maxRotation: 0,
            autoSkip: true,
            font: {
                size: 9
            }
        },
        grid: {
            display: false,
            drawBorder: false,
            tickLength: 0
        }
    }  
}

// config 
const config = {
    type: 'matrix',
    data,
    options: {
        maintainAspectRatio: false,
        scales: scales,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    title: function (tooltipItems) {
                        // Customize the title of the tooltip to display 'tasks value of the day'
                        return `Task: ${tooltipItems[0].raw.v}`;
                    },
                    label: function (tooltipItem) {
                        // Customize the content of each tooltip label to display 'the date of the day'
                        return `Date: ${tooltipItem.raw.x}`;
                    }
                }
            }
        }
    }
};

// render init block
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);

// Instantly assign Chart.js version
const chartVersion = document.getElementById('chartVersion');
chartVersion.innerText = Chart.version;
