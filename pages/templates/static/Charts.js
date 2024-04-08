
function getRandomRGBColor() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);

    return 'rgb(' + r + ',' + g + ',' + b + ')';
}

function createBarChart(data, timeperiod) {
    var layout = {
        title: ` Wiki revision count for each Event within ${timeperiod} of the event occurred (click on the bar for further drill down)`,
        yaxis: { title: 'Total Wiki Revisions' },
        xaxis: {
            title: 'Event',
            tickangle: 4  // Rotates the x-axis labels
        },

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
        title: `Rivision distribution across Wiki Pages`,
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
    var totalRevSticker = `Total Revision Count: ${totalRevCount} `
    var tags = Object.keys(tagCount)
    percentages = tags.map((tag) => `${tagCount[tag]} (${roundNumber(tagCount[tag] / totalRevCount)}%)`)

    var trace1 = {
        x: Object.keys(tagCount),
        y: tags.map((tag) => tagCount[tag]),
        name: 'Tag',
        type: 'bar',
        hovertemplate: totalRevSticker + ' <br> %{x}: %{y}  <extra></extra>',
        hoverinfo: percentages.map(String),
        textposition: 'auto',

    };

    var trace2 = {
        x: tags,
        y: tags.map((tag) => totalRevCount - tagCount[tag]),
        hoverinfo: 'none',
        name: 'Total Revision Count',
        type: 'bar',

    };

    var data = [trace1, trace2];

    var layout = { barmode: 'stack', 'title': 'Rivision distribution across Tags' };

    Plotly.newPlot('donutChart', data, layout);


}   
