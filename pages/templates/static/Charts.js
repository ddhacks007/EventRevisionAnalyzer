
function getRandomRGBColor() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);

    return 'rgb(' + r + ',' + g + ',' + b + ')';
}

function createBarChart(data, timeperiod) {
    var layout = {
        title: ` Wiki revision count for each Event within ${timeperiod} of the event occurred (click on the bar for further drill down)`,
        xaxis: { title: 'Event' },
        yaxis: { title: 'Total Wiki Revisions' }
    };
    var traces = [];
    var xValues = [];
    var yValues = [];
    var hoverTexts = [];

    Object.keys(data).sort().forEach(function (event) {
        xValues.push(event);
        yValues.push(data[event]['total_count']);
        console.log(data[event])
        console.log(Object.keys(data[event]).map(function (title) {
            return title + ': ' + data[event][title]['count'];
        }).join("<br>"))
        var hoverText = Object.keys(data[event]).filter((val) => val != "total_count").map(function (title) {
            return title + ': ' + data[event][title]['count'];
        }).join("<br>");
        hoverTexts.push(hoverText)
        console.log(hoverTexts)
    });

    var cData = [{
        x: xValues,
        y: yValues,
        type: 'bar',
        text: hoverTexts,
        marker: {
            "color": Object.keys(data).map((event) => getRandomRGBColor())
        }
    }]
    console.log(traces)

    Plotly.newPlot('barChart', cData, layout);
    document.getElementById('barChart').on('plotly_click', function (data) {
        var point = data.points[0];
        pages = point.text.split("<br>").map((pageCount) =>
            pageCount.split(" ")[0].replace(":", ""));
        counts = point.text.split("<br>").map((pageCount) =>
            parseInt(pageCount.split(" ")[1]))
        createPieChart(pages, counts, point.x);
        createDonetChart(eventTagCount[point.x], point.y)

    });
}

function createPieChart(pages, counts, event) {
    var layout = {
        title: `Wiki Page Distribution`,
        xaxis: { title: 'Event' },
        yaxis: { title: 'Total Wiki Count' }
    };
    var data = [{
        values: counts,
        labels: pages,
        type: 'pie',
        marker: {
            colors: Object.keys(pages).map((page) => getRandomRGBColor())

        },
    }];

    Plotly.newPlot('pieChart', data, layout);

}

function createDonetChart(tagCount, totalRevCount) {
    var layout = {
        title: `Tag Distribution`,
        xaxis: { title: 'Tag' },
        yaxis: { title: 'Total Wiki Count' }
    };

    var counts = Object.keys(tagCount).map((tag) => tagCount[tag]);
    var labels = Object.keys(tagCount).map((tag) => tag);

    var data = [
        {
            values: counts,
            labels: labels,
            type: 'pie',

        }
    ];

    Plotly.newPlot('donutChart', data, layout);

}   
