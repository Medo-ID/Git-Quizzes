// JS 
var chart = JSC.chart('chartDiv', { 
    debug: true, 
    type: 'calendar week30min solid', 
    data: './resources/heatmaptracking_data.csv', 
    calendar: { calculation: 'average' }, 
    legend: { 
        template: '%name,%icon', 
        position: 'bottom', 
        cellSpacing: 1, 
        defaultEntry_icon_width: 10 
    }, 
    defaultPoint_tooltip: '{%date:date f}', 
    palette: { 
        colors: ['#00897b', '#e0e0e0', '#ffa000'], 
        ranges: [ 
        { 
            value: 0, 
            legendEntry: { 
            name: 'Sleep: ', 
            style_fontWeight: 'bold', 
            style_fontSize: 12 
            } 
        }, 
        { value: 1 }, 
        { value: 2 }, 
        { value: 3 }, 
        { value: 4 }, 
        { value: 5 }, 
        { 
            value: 6, 
            legendEntry: { 
            name: ' Inactive: ', 
            style_fontWeight: 'bold', 
            style_fontSize: 12 
            } 
        }, 
        { 
            value: 7, 
            legendEntry: { 
            name: ' Active: ', 
            style_fontWeight: 'bold', 
            style_fontSize: 12 
            } 
        }, 
        { value: 8 }, 
        { value: 9 }, 
        { value: 10 }, 
        { value: 11 }, 
        { value: 12 } 
        ] 
    }, 
    xAxis: { 
        scale_interval: 2, 
        defaultTick: { 
        label_text: function(v) { 
            return ((v % 24) / 2).toString(); 
        }, 
        gridLine_width: 0 
        }, 
        customTicks: [ 
        { 
            value: 0, 
            label_text: 
            '<icon name=weather/moon size=18 fill=#14327f><br>AM'
        }, 
        //24 == 12PM because there are 48 30min intervals in a day 
        { 
            value: 24, 
            label_text: 
            '<icon name=weather/sun size=24 fill=#e9b82e><br>PM'
        } 
        ] 
    }, 
    
    defaultSeries_legendEntry_visible: false, 
    toolbar_visible: false
}); 