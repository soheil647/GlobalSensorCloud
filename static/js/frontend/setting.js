import {GetRequest} from "./requests.js";


const getGeneralDefault = () => {
    GetRequest('/frontend/setting/default/')
        .then(resp => {
            document.getElementById('general-nuisance').value = resp['nuisanceAlarmThreshold']
            document.getElementById('general-training').value = resp['trainingPeriod']
            document.getElementById('general-operation').value = resp['normalPeriod']

            let select = document.getElementById('general-sensitivity')
            select.value = resp['anomalySensitivity']
        })
        .catch(error => {
            console.log(error)
        })
}

// const getAiModels = () => {
//     GetRequest('/frontend/setting/devices/')
//         .then(resp => {
//             // console.log(resp['devices'])
//             let select = document.getElementById('setting-devices')
//
//             for (let device of resp['devices']) {
//                 let option = document.createElement('option');
//                 option.value = device
//                 option.innerText = device
//                 select.appendChild(option);
//             }
//         })
//         .catch(error => {
//             console.log(error)
//         })
// }

$(document).ready(function () {
    $('#table-device-anomalies').DataTable({
        ajax: {
            url: '/frontend/setting/devices/',
            dataSrc: 'devices'
        },
        columnDefs: [{"defaultContent": "-", "targets": "_all"}],
        columns: [
            {data: 'name'},
            {
                data: 'name',
                render: function (data, type, full, meta) {
                    return '<button id="setting-devices" onclick=DeviceSelect(this.value) value="' + data + '">Show Detail</button>'
                },
            },
        ],
        order: [[0, 'desc']],
        responsive: true,
        bPaginate: false,
        scrollY: 200,
        pageLength: 50
    });
});

getGeneralDefault()
// getAiModels()
