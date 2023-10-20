from django.shortcuts import redirect
from urllib.parse import urlencode
from django.utils.http import url_has_allowed_host_and_scheme


class AppendVehicleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        vehicle = request.GET.get('vehicle')
        organization = request.GET.get('organization')
        NoVehicle = request.GET.get('hide')

        if NoVehicle:
            return self.get_response(request)

        if vehicle is not None and organization is not None and NoVehicle is None:
            # If 'vehicle' parameter is present in this request, save it in the session
            request.session['vehicle'] = vehicle
            request.session['organization'] = organization
        else:
            # If 'vehicle' is not in this request, but is in the session, get it from the session
            vehicle = request.session.get('vehicle')
            organization = request.session.get('organization')

        if vehicle and 'vehicle' not in request.GET and not request.path.startswith('/admin') and not request.path.startswith('/users') and NoVehicle is None:
            # Add 'vehicle' parameter to URL only if it's not already present in the request
            url = request.path_info
            querystring = request.GET.copy()
            querystring['vehicle'] = vehicle
            querystring['organization'] = organization
            new_url = f"{url}?{urlencode(querystring)}"

            if not url_has_allowed_host_and_scheme(
                    url=new_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
            ):
                return self.get_response(request)

            return redirect(new_url)

        return self.get_response(request)
