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
const dataElement = document.getElementById('data');
const user_data = dataElement.dataset.message;

// Now you can use the 'message' variable in your JavaScript code
console.log('Message from the server:', user_data);

// chart config
// date settings
function isoDaysOfWeek(dt){
    let weekdays = dt.getDay(); //0 to 6, from sunday
    weekdays = (weekdays + 6) % 7 + 1; //1 to 7 starting week monday
    return '' + weekdays;
}

// setup date: 365 days/squares
function generateDays() {
    const day = new Date();
    const today = new Date(day.getFullYear(), day.getMonth(), day.getDate(), 0, 0, 0, 0);
    const data_user = [];

    let dt = new Date(new Date().setDate(today.getDate() - 365));

    while (dt <= today) {
        const iso = dt.toISOString().substr(0, 10);
        const dayOfWeek = isoDaysOfWeek(dt);

        // Use a different ISO string for each day of the week
        const isoForWeek = iso + 'T00:00:00'; 

        data_user.push({
            x: isoForWeek,
            y: dayOfWeek,
            d: iso,
            v: Math.round(Math.random() * 6)
        });

        dt = new Date(dt.setDate(dt.getDate() + 1));
    }

    console.log(data_user);
    return data_user;
}
// setup blocks
const data = {
    datasets: [{
        label: 'Track your daily activities',
        data: generateDays(),
        backgroundColor(color){
            const value = color.dataset.data[color.dataIndex].v;
            const transparency = (value / 7).toFixed(2);
            return `rgba(238, 108, 77, ${transparency})`;
        },
        borderColor: 'rgb(47, 47, 47)',
        borderRadius: 1,
        borderWidth: 1,
        hoverBackgroundColor: 'rgb(53, 79, 82)',
        hoverBorderColor: 'rgb(252, 225, 199)',
        width(c){
            const a = c.chart.chartArea || {};
            return (a.right - a.left) / 53 - 1;
        },
        height(c){
            const a = c.chart.chartArea || {};
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
        position: 'bottom',
        offset: true,
        time: {
            unit: 'week',
            round: 'day',
            isoWeekDay: 1,
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
