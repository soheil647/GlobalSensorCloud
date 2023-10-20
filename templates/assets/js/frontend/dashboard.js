const urlParams = new URLSearchParams(window.location.search);
const organizationParam = urlParams.get('organization');
const vehicleIdParam = urlParams.get('vehicle');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const getAggrTitle = (aggr) => {
    if (aggr === 'daily' || aggr === null) {
        return 'Per Day'
    } else if (aggr === 'weekly') {
        return 'Per Week'
    } else {
        return 'Per Month'
    }
}

const drawChartBreaks = (aggr) => {

    $("canvas#brakes-canvas").remove();
    $("div#brakes-report").append('<canvas id="brakes-canvas" height="200px"></canvas>');

    const ctx = document.getElementById('brakes-canvas');

    const aggr_title = getAggrTitle(aggr)

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 1999, 2050],
            datasets: [{
                data: [2, 5, 3, 10, 15, 13, 27, 11, 22, 16],
                label: "# of Breaks",
                borderColor: "#3e95cd",
                fill: false
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Number of Brakes ' + aggr_title,
                    align: 'center',
                    color: 'blue',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

const drawChartIncidents = (aggr) => {

    $("canvas#incidents-canvas").remove();
    $("div#incident-report").append('<canvas id="incidents-canvas" height="100px"></canvas>');
    const ctx = document.getElementById('incidents-canvas');

    const aggr_title = getAggrTitle(aggr)
    let labels = [];
    let date = new Date();

    for (let i = 0; i < 10; i++) {
        switch (aggr_title) {
            case 'Per Day':
                labels.push(date.toISOString().slice(0, 10));
                date.setDate(date.getDate() - 1);
                break;
            case 'Per Week':
                labels.push(`${date.toISOString().slice(0, 10)}`);
                date.setDate(date.getDate() - 7);
                break;
            case 'Per Month':
                labels.push(`${date.toISOString().slice(0, 7)}`);
                date.setMonth(date.getMonth() - 1);
                break;
        }
    }
    if (aggr == null) {
        aggr = 'daily'
    }
    $.ajax({
        url: `api/incidents/?mode=${aggr}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
        type: 'get',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (data) {
            //console.log(data)
            let counts = Array(10).fill(0);
            data.forEach(incident => {
                let timestamp_utc = new Date(incident.timestamp);

                let year = timestamp_utc.getFullYear();
                let month = String(timestamp_utc.getMonth() + 1).padStart(2, '0'); // months are 0-based in JS
                let day = String(timestamp_utc.getDate()).padStart(2, '0');

                let timestamp = new Date(`${year}-${month}-${day}`);

                for (let i = 0; i < 10; i++) {
                    if (aggr_title === 'Per Day' && timestamp.toISOString().slice(0, 10) === labels[i]) {
                        counts[i]++;
                    } else if (aggr_title === 'Per Week' && timestamp >= new Date(labels[i]) && timestamp < new Date(labels[i - 1])) {
                        counts[i]++;
                    } else if (aggr_title === 'Per Month' && timestamp.toISOString().slice(0, 7) === labels[i]) {
                        counts[i]++;
                    }
                }
            });
            console.log(labels)
            console.log(counts)

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels.reverse(),
                    datasets: [{
                        data: counts.reverse(),
                        label: "# of Events",
                        borderColor: "#3e95cd",
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            suggestedMax: 5,
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Number of Events ' + aggr_title,
                            align: 'center',
                            color: 'blue',
                            font: {
                                size: 16
                            }
                        }
                    }
                }
            });

        },
        fail: error => {
            console.log(error)
        }
    });
}

HandleAggrChange = (value) => {
    drawChartIncidents(value)
}

function fetchVehicleInfo() {
    $.ajax({
        url: `api/vehicle_info/?vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
        type: 'get',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (data) {
            document.getElementById('longitude').innerText = parseFloat(data['longitude']).toFixed(1);
            document.getElementById('latitude').innerText = parseFloat(data['latitude']).toFixed(1);
            document.getElementById('speed').innerText = parseFloat(data['speed']).toFixed(1);

            let zoneArray = data['zones'].split(',').map(Number);
            zoneArray.forEach((zone, index) => {
                // Construct the cell's id based on the current index (index + 1 because it starts from cell1)
                let cellId = "cell" + (index + 1);

                // Get the cell element by its id
                let cellElement = document.getElementById(cellId);

                // Update the fill color based on the zone value
                if (zone === 0) {
                    cellElement.setAttribute('fill', '#BCFFA4');
                } else {
                    if ([2, 3, 6, 7].includes(index + 1)) {
                        cellElement.setAttribute('fill', 'red');
                    } else {
                        cellElement.setAttribute('fill', 'orange');
                    }
                }
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('Error:', errorThrown);
        }
    });
}

// drawChartBreaks('daily')
drawChartIncidents('daily')
setInterval(fetchVehicleInfo, 1000);