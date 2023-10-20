// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
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

const post = (apiUrl, payload) => {
    let resp = null;
    $.ajax({
        url: apiUrl,
        type: 'post',
        data: JSON.stringify(payload),
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (data) {
            // console.log(data)
            // resp = JSON.parse(JSON.stringify(data));
        },
        fail: error => {
            console.log(error)
        }
    });
    return post
}


function SaveGeneral() {

    const training = document.getElementById('general-training').value;
    const alarm = document.getElementById('general-nuisance').value;
    const normal = document.getElementById('general-operation').value;
    const sensitivity = document.getElementById('general-sensitivity').value;

    const payload = {
        trainingPeriod: training,
        nuisanceAlarmThreshold: alarm,
        normalPeriod: normal,
        anomalySensitivity: sensitivity
    }
    post('/frontend/setting/save/default/', payload)

}

function SaveSpecific() {

    const device = document.getElementById('single-device-name').value
    const training = document.getElementById('specific-training').value;
    const alarm = document.getElementById('specific-nuisance').value;
    const normal = document.getElementById('specific-operation').value;
    const sensitivity = document.getElementById('specific-sensitivity').value;

    const payload = {
        device: device,
        trainingPeriod: training,
        nuisanceAlarmThreshold: alarm,
        normalPeriod: normal,
        anomalySensitivity: sensitivity
    }
    post('/frontend/setting/save/device/', payload)

}

const DeviceSelect = device_select => {
    // console.log(device_select)
    const payload = {
        name: device_select,
    }
    $.ajax({
        url: '/frontend/setting/devices/values/',
        type: 'post',
        data: JSON.stringify(payload),
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (data) {
            document.getElementById('specific-training').value = data['trainingPeriod'];
            document.getElementById('specific-nuisance').value = data['nuisanceAlarmThreshold'];
            document.getElementById('specific-operation').value = data['normalPeriod'];
            document.getElementById('specific-sensitivity').value = data['anomalySensitivity'];

            document.getElementById("device-name").innerText = device_select
            document.getElementById("single-device-name").value = device_select

            document.getElementById('device-settings').style.display = 'block'
        },
        fail: error => {
            console.log(error)
        }
    });
}

ChangeSaveGeneral = () => {
    document.getElementById("generalDefaultBottom").innerText = "Save Changes!"
    document.getElementById("generalDefaultBottom").style.background= "#464F52FF"
}
ChangeSaveSpecific = () => {
    document.getElementById("specificDefaultBottom").innerText = "Save Changes!"
    document.getElementById("specificDefaultBottom").style.background= "#464F52FF"
}