HandleOrganizationChange = (value) => {
    if (value === "") {
        let urlParams = new URLSearchParams(window.location.search);

        urlParams.set('hide', "true");
        urlParams.delete('vehicle');
        urlParams.delete('organization');
        // Get the current URL without any query parameters or hash
        // const baseUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;

        // Use the history API to replace the current URL

        window.location.search = urlParams.toString();
        // window.history.replaceState({}, '', baseUrl);
        // Set the window's location to the base URL
        // window.location.href = baseUrl;
    }
    let select = document.getElementById('selectVehicle')
    while (select.options.length > 1) {
        select.remove(select.options.length - 1);
    }

    $.ajax({
        url: 'cloud/api/index/vehicles/?vehicleOrganization=' + value,
        type: 'get',
        headers: {
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (vehicles) {

            let option = document.createElement('option');
            option.value = ""
            option.innerText = "Select a Vehicle"
            option.disabled = true
            option.selected = true
            select.appendChild(option);

            for (let vehicle of vehicles) {
                let option = document.createElement('option');
                option.value = vehicle["vehicleId"]
                option.innerText = vehicle["vehicleId"]
                select.appendChild(option);
            }
            document.getElementById('vehicleDiv').style.display = 'block'
        },
        fail: error => {
            console.log(error)
        }
    });
}

HandleOrganizationSelect = () => {
    let select = document.getElementById('selectOrganization')
    if (select === null) return;

    $.ajax({
        url: 'cloud/api/index/vehicles/',
        type: 'get',
        headers: {
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (vehicles) {
            let organizations = [];
            for (let vehicle of vehicles) {
                if(organizations.includes(vehicle['organization'])) { continue; }
                organizations.push(vehicle['organization'])
                let option = document.createElement('option');
                option.value = vehicle["organization"]
                option.innerText = vehicle["organization"]
                select.appendChild(option);
            }
            let option = document.createElement('option');
            option.value = ""
            option.innerText = "No Org"
            select.appendChild(option);

            const urlParams = new URLSearchParams(window.location.search);
            const organizationParam = urlParams.get('organization');

            if (organizationParam){
                select.value = organizationParam
            }
        },
        fail: error => {
            console.log(error)
        }
    });
}

HandleVehicleSelect = () => {
    let select = document.getElementById('selectVehicle')

    const urlParams = new URLSearchParams(window.location.search);
    const organizationParam = urlParams.get('organization');
    let organization = ''
    if (organizationParam) {
        organization = organizationParam;
    } else {
        organization = userOrganization;
    }

    $.ajax({
        url: 'cloud/api/index/vehicles/?vehicleOrganization=' + organization,
        type: 'get',
        headers: {
            'Content-type': 'application/json'
        },
        dataType: 'json',
        success: function (vehicles) {
            console.log(vehicles)
            let option = document.createElement('option');
            option.value = ""
            option.innerText = "Select a Vehicle"
            option.disabled = true
            option.selected = true
            select.appendChild(option);

            const urlParams = new URLSearchParams(window.location.search);
            for (let vehicle of vehicles) {
                let option = document.createElement('option');
                option.value = vehicle["vehicleId"]
                option.innerText = vehicle["vehicleId"]
                select.appendChild(option);
            }
            const vehicleParam = urlParams.get('vehicle');
            if (vehicleParam){
                document.getElementById('vehicleDiv').style.display = 'block'
                select.value = vehicleParam
                // document.getElementById('selectVehicle').value = vehicleParam
            }
        },
        fail: error => {
            console.log(error)
        }
    });
}

HandleVehicleChange = (selected_vehicle) => {
    const organization_element = document.getElementById('selectOrganization')
    let organization = ''
    if (organization_element) {
        organization = organization_element.value;
    } else {
        organization = userOrganization;
    }

    if (selected_vehicle === "") {
        const url = new URL(window.location.href);
        const params = new URLSearchParams(url.search);
        params.delete('vehicle');
        params.delete('hide');
        url.search = params.toString();
        window.history.replaceState({}, '', url.href);
    } else {
        let urlParams = new URLSearchParams(window.location.search);
        urlParams.set('vehicle', selected_vehicle);
        urlParams.set('organization', organization);
        urlParams.delete('hide');
        window.location.search = urlParams.toString();
    }
}

HandlePagesActive = () => {
    let links = document.querySelectorAll('.myLink');
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('vehicle')) {
        for (let i = 0; i < links.length; i++) {
            links[i].removeEventListener('click', function (event) {
                event.preventDefault();
            });
        }
    } else {
        for (let i = 0; i < links.length; i++) {
            links[i].addEventListener('click', function (event) {
                event.preventDefault();
            });
        }
    }
}
HandlePagesActive()
HandleOrganizationSelect()
HandleVehicleSelect()

