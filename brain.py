import json
import paho.mqtt.client as mqtt
from celery import Celery
from datetime import datetime, timezone, timedelta
import os
import django
import time
from django.utils import timezone

verbose = 1
monitor = 1
step_time = 1


def load_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
        verbose = config['tof_camera_configuration']['verbose']
        monitor = config['general_configuration']['monitor']
        return verbose


# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GlobalSensorCloud.settings')

# Initialize Django app
django.setup()

from tof.models import TofData, TofData1, TofData2, VizData, LdrData
from tof.tasks import process_data, create_incident, vehicle_data

# MQTT broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = ['towebapp']

# Initialize Celery instance
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Initialize message count and timestamp for each topic
message_counts = {topic: 0 for topic in MQTT_TOPICS}
last_message_times = {topic: time.time() for topic in MQTT_TOPICS}

# Define a flag to indicate if we are currently in an incident state
incident_state = False

# Define a timestamp to indicate when the incident state started
incident_start_time = datetime.now(timezone.utc)

# Define a time interval to disable incident reporting after an incident is detected
incident_disable_interval = timedelta(seconds=5)


# Define callback function for when a message is received
def on_message(client, userdata, message):
    global incident_state
    global incident_start_time

    try:
        payload = json.loads(message.payload)
        timestamp = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')

        # Determine which topic the message was received on
        for topic in MQTT_TOPICS:
            if message.topic == 'towebapp':
                if time.time() - last_message_times[topic] > step_time:
                    tofm = payload['tofm']
                    tofl = payload['tofl']
                    tofr = payload['tofr']
                    viz = payload['viz']
                    ldr_decision = payload['ldr decision']
                    zones = payload['zones']
                    ldr_values = payload['ldr values']
                    gps = payload['gps']
                    offset = payload['h_offset']

                    sensor_topic_list = ['tofm', 'tofl', 'tofr', 'viz', 'ldr values']
                    for sensor_topic in sensor_topic_list:
                        process_data.delay(timestamp, payload[sensor_topic], sensor_topic)

                    vehicle_data.delay(timestamp, payload)
                    last_message_times[topic] = time.time()

                    if incident_state:
                        # Check if the incident disable interval has elapsed
                        if datetime.now(timezone.utc) >= incident_start_time + incident_disable_interval:
                            # Disable the incident state
                            incident_state = False
                            incident_start_time = None

                    if (viz and viz.get('value1') == 2) or \
                            (tofl and tofl.get('value1') == 2) or \
                            (tofr and tofr.get('value1') == 2) or \
                            (tofm and tofm.get('value1') == 2) or \
                            (ldr_decision and ldr_decision == 2):

                        # Set the incident state flag and start the incident disable interval
                        incident_start_time = datetime.now(timezone.utc)


                        # Send the brake signal (placeholder code)
                        if verbose:
                            print("Brake signal sent")

                        client.publish("control", "2")
                        if not incident_state:
                            incident_state = True
                            # Call the create_incident function through Celery
                            create_incident.delay(timestamp, payload)

                    elif (viz and viz.get('value1') == 1) or \
                            (tofl and tofl.get('value1') == 1) or \
                            (tofr and tofr.get('value1') == 1) or \
                            (tofm and tofm.get('value1') == 1) or \
                            (ldr_decision and ldr_decision == 1):
                        if not incident_state:
                            client.publish("control", "1")

                    else:
                        if not incident_state:
                            client.publish("control", "0")

            if verbose:
                print(topic, payload)
    except Exception as e:
        print("Error occurred in brain:", str(e))


verbose = load_config()
print("loaded verbose is:", verbose)

# Create MQTT client instance
client = mqtt.Client()

# Set callback function
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT)

# Subscribe to MQTT topics
for topic in MQTT_TOPICS:
    client.subscribe(topic)

# Start the MQTT loop
client.loop_forever()
