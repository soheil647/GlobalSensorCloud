from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import TofData, TofData1, TofData2, VizData, LdrData, IncidentData, VehicleInfo
from datetime import timedelta, datetime

# Initialize message counter and step size
MESSAGE_COUNTER = 0
STEP_SIZE = 1


@shared_task
def vehicle_data(timestamp, data):

    latitude = data['gps']['Precise Latitude']
    longitude = data['gps']['Precise Longitude']
    speed = data['gps']['Speed']
    zones = data['zones']
    VehicleInfo.objects.create(timestamp=timestamp, latitude=latitude, longitude=longitude, speed=speed,
                               zones=','.join(map(str, zones)))
    return 'Vehicle Info Saved'


@shared_task
def process_data(timestamp, data, topic):
    global MESSAGE_COUNTER

    # Increment message counter
    MESSAGE_COUNTER +=1

    # Only process and save message if it matches the step size
    if MESSAGE_COUNTER % STEP_SIZE == 0:
        print(topic, data)

        # Use topic to determine which model to use for storing data
        if topic in ['tofm', 'tofl', 'tofr', 'viz']:
            value1 = data.get('value1')
            value2 = data.get('value2')
            value3 = data.get('value3')

            if topic == 'tofm':
                new_data = TofData.objects.create(timestamp=timestamp, value1=value1, value2=value2, value3=value3)
            elif topic == 'tofl':
                new_data = TofData1.objects.create(timestamp=timestamp, value1=value1, value2=value2, value3=value3)
            elif topic == 'tofr':
                new_data = TofData2.objects.create(timestamp=timestamp, value1=value1, value2=value2, value3=value3)
            elif topic == 'viz':
                new_data = VizData.objects.create(timestamp=timestamp, value1=value1, value2=value2, value3=value3)
            else:
                print('Topic is Invalid: ', topic)
                raise ValueError('Invalid topic')

        elif topic == 'ldr values':
            new_data = LdrData.objects.create(timestamp=timestamp, value1=data[0], value2=data[1], value3=data[2],
                                              value4=data[3], value5=data[4], value6=data[5], value7=data[6],
                                              value8=data[7], value9=data[8], value10=data[9])
        else:
            print('Topic is Invalid: ', topic)
            raise ValueError('Invalid topic')

        # Save data to database
        new_data.save()

        # Reset message counter if it reaches the step size
        if MESSAGE_COUNTER == STEP_SIZE:
            MESSAGE_COUNTER = 0
        return 'Sensor Data Saved'


@shared_task
def create_incident(timestamp, payload):
    print(timestamp)
    print('Creating Incident!')
    timestamp_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

    # Get current GPS coordinates (placeholder)
    latitude = payload['gps']['Precise Latitude']
    longitude = payload['gps']['Precise Longitude']

    # Get current speed (placeholder)
    speed = payload['gps']['Speed']

    # Placeholder values for breakAction, override, and zones
    break_action = True
    override = False
    zones = payload['zones']

    latest_tofm = TofData.objects.latest('id')
    latest_tofl = TofData1.objects.latest('id')
    latest_tofr = TofData2.objects.latest('id')
    latest_viz = VizData.objects.latest('id')
    latest_ldr = LdrData.objects.latest('id')

    # Create a new incident record
    incident = IncidentData.objects.create(
        timestamp=timestamp_date,
        description='Obstacle detected',
        LdrValue=latest_ldr,
        TofmValue=latest_tofm,
        ToflValue=latest_tofl,
        TofrValue=latest_tofr,
        VizValue=latest_viz,
        latitude=latitude,
        longitude=longitude,
        breakAction=break_action,
        override=override,
        speed=speed,
        zones=','.join(map(str, zones))
    )
    incident.save()
    print('Incident Saved')

    return "DONE saving Incident!"
