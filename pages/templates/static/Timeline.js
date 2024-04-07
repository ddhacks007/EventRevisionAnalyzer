

function createTraces(data) {
    const traces = [];
    for (const title in data) {
        if (data.hasOwnProperty(title)) {
            const dates = Object.keys(data[title]);
            const counts = Object.values(data[title]);

            const trace = {
                x: dates,
                y: counts,
                mode: 'lines+markers',
                connectgaps: true,
                name: title
            };

            traces.push(trace);
        }
    }
    return traces;
}

function createTimeLine(data) {
    const traces = createTraces(data);

    const layout = {
        title: 'Revision Counts by Date for Each Title',
        xaxis: {
            title: 'Date'
        },
        yaxis: {
            title: 'Count'
        },
        showlegend: true
    };

    Plotly.newPlot('timeline', traces, layout);

}
