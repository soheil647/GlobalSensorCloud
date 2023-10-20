const urlParams = new URLSearchParams(window.location.search);
const organizationParam = urlParams.get('organization');
const vehicleIdParam = urlParams.get('vehicle');

drawDataTable = () => {
    $('#incidents').DataTable({
        ajax: {
            url: `/api/incidents/?vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
            dataSrc: ''
        },
        columnDefs: [{"defaultContent": "-", "targets": "_all"}],
        columns: [
            {data: 'timestamp'},
            {data: 'description'},
            // {data: 'value1'},
            // {data: 'value2'},
            // {data: 'value3'},
            // {data: 'value4'},
            // {data: 'value5'},
            {
                data: 'id',
                render: function (data, type, full, meta) {
                    return '<button class="btn btn-sm btn-primary" onclick="HandleIncidentButton(' + data + ')">Show Detail</button>'
                },
            },
            // {data: 'latitude'},
            // {data: 'longitude'},
            // {data: 'breakAction'},
            // {data: 'override'},
            // {data: 'speed'},
            // {data: 'zone_coord1'},
            // {data: 'zone_coord2'},
            // {data: 'zone'},
        ],
        order: [[0, 'desc']],
        responsive: true,
        // scrollX: true
    });
}

drawDetailSensorDataTable = (table_id, sensor_name, timestamp) => {
    console.log(table_id, sensor_name)

    $('#' + table_id).DataTable({
        ajax: {
            url: `/api/incidentsensordata/?name=${sensor_name}&timestamp=${timestamp}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
            dataSrc: ''
        },
        columnDefs: [{"defaultContent": "-", "targets": "_all"}],
        columns: [
            {data: 'timestamp'},
            {data: 'value1'},
            {data: 'value2'},
            {data: 'value3'}
        ],
        order: [[0, 'desc']],
        responsive: true,
        paging: false,
        pageLength: 3,
        // ordering: false,
        info: false,
        searching: false,
    }).page.len(5).draw();
}

let timestamp_global = null
drawDetailSensorDataTableLdr = (table_id, sensor_name, timestamp) => {
    console.log(table_id, sensor_name)
    timestamp_global = timestamp
    $('#' + table_id).DataTable({
        ajax: {
            url: `/api/incidentsensordata/?name=${sensor_name}&timestamp=${timestamp}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
            dataSrc: ''
        },
        columnDefs: [{"defaultContent": "-", "targets": "_all"}],
        columns: [
            {data: 'timestamp'},
            {data: 'value1'},
            {data: 'value2'},
            {data: 'value3'},
            {data: 'value4'},
            {data: 'value5'},
            {data: 'value6'},
            {data: 'value7'},
            {data: 'value8'},
            {data: 'value9'},
            {data: 'value10'}
        ],
        order: [[0, 'desc']],
        responsive: true,
        paging: false,
        drawCallback: function () {
            $(this).find('tbody tr').hide();
            $(this).find('tbody tr:lt(3)').show();
        },
        pageLength: 3,
        // ordering: false,
        info: false,
        searching: false,
    })
}

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

HandleIncidentButton = (incidentId) => {
    console.log(incidentId)
    document.getElementById('incident-detail').style.display = 'block'
    // document.getElementById('video').href = `api/download_video/?incident_id=${incidentId}`

    let table_ldr = $('#table-sensor-data-ldr').DataTable()
    table_ldr.clear()
    table_ldr.destroy()

    let table_tof = $('#table-sensor-data-tof').DataTable()
    table_tof.clear()
    table_tof.destroy()

    let table_viz = $('#table-sensor-data-vis').DataTable()
    table_viz.clear()
    table_viz.destroy()

    $.ajax({
        url: `api/incidents/?incident_id=${incidentId}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
        type: 'get',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (data) {
            console.log(data[0]);

            let zoneArray = data[0]['zones'].split(',').map(Number);
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

            drawDetailSensorDataTableLdr('table-sensor-data-ldr', 'ldr1', data[0]['timestamp'])
            drawDetailSensorDataTable('table-sensor-data-vis', 'visual', data[0]['timestamp'])
            drawDetailSensorDataTable('table-sensor-data-tof', 'tof', data[0]['timestamp'])
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('Error:', errorThrown);
        }
    });
}

HandleToFSelect = (tofCamera) => {
    console.log(tofCamera)
    let table = $('#table-sensor-data-tof').DataTable()
    table.clear()
    table.destroy()

    drawDetailSensorDataTable('table-sensor-data-tof', tofCamera, timestamp_global)
}

HandleLdrSelect = (ldrNumber) => {
    console.log(ldrNumber)
    let table = $('#table-sensor-data-ldr').DataTable()
    table.clear()
    table.destroy()

    drawDetailSensorDataTableLdr('table-sensor-data-ldr', ldrNumber)
}

drawDataTable()