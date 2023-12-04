const urlParams = new URLSearchParams(window.location.search);
const organizationParam = urlParams.get('organization');
const vehicleIdParam = urlParams.get('vehicle');

HandleToFSelect = (tofCamera) => {
    console.log(tofCamera)
    let table = $('#table-sensor-data-tof').DataTable()
    table.clear()
    table.destroy()

    drawDataTable('table-sensor-data-tof', tofCamera)
}

HandleLdrSelect = (ldrNumber) => {
    console.log(ldrNumber)
    let table = $('#table-sensor-data-ldr').DataTable()
    table.clear()
    table.destroy()

    drawDataTable('table-sensor-data-ldr', ldrNumber)
}

function handleButtonClick(buttonId) {
    let tof_div = document.getElementById('tof-div')
    let vis_div = document.getElementById('vis-div')
    let ldr_div = document.getElementById('ldr-div')

    if (buttonId === 'tof') {
        tof_div.style.display = 'block'

        let table = $('#table-sensor-data-tof').DataTable()
        table.clear()
        table.destroy()
        drawDataTable('table-sensor-data-tof', 'tof')
    } else {
        tof_div.style.display = 'none'
    }

    if (buttonId === 'visual') {
        vis_div.style.display = 'block'
        let table = $('#table-sensor-data-visual').DataTable()
        table.clear()
        table.destroy()
        drawDataTable('table-sensor-data-visual', 'visual')
    } else {
        vis_div.style.display = 'none'
    }

    if (buttonId === 'ldr') {
        ldr_div.style.display = 'block'
        let table = $('#table-sensor-data-ldr').DataTable()
        table.clear()
        table.destroy()
        drawDataTable('table-sensor-data-ldr', 'ldr1')
    } else {
        ldr_div.style.display = 'none'
    }
}


drawDataTable = (table_id, sensor_name) => {
    if (sensor_name === 'ldr') {

        $('#' + table_id).DataTable({
            ajax: {

                url: `/api/sensordata/?name=${sensor_name}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
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
                {data: 'value10'},
            ],
            order: [[0, 'desc']],
            responsive: true,
        });
    } else {
        $('#' + table_id).DataTable({
            ajax: {

                url: `/api/sensordata/?name=${sensor_name}&vehicleId=${vehicleIdParam}&organization=${organizationParam}`,
                dataSrc: ''
            },
            columnDefs: [{"defaultContent": "-", "targets": "_all"}],
            columns: [
                {data: 'timestamp'},
                {data: 'value1'},
                {data: 'value2'},
                {data: 'value3'},
            ],
            order: [[0, 'desc']],
            responsive: true,
        });
    }
}


// drawDataTable('table-sensor-data-vis', 'visual')
// drawDataTable('table-sensor-data-ldr', 'ldr')
// drawDataTable('table-sensor-data-tof2', 'tof1')
// drawDataTable('table-sensor-data-tof3', 'tof2')