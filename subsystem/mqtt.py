import paho.mqtt.client as mqtt
from django.conf import settings

from .models import Sensor, SensorLog

def on_message_mqtt(sensor_name):
    def template(client, userdata, msg):
        sen = Sensor.objects.get(name=sensor_name)
        sen.value = msg.payload.decode('utf-8')
        sen.save()
        sen_log = SensorLog(name=sen, value=msg.payload.decode('utf-8'))
        sen_log.save()
    return template

def on_connect(client, userdata, rc, result):
    client.subscribe('sfarm/#')

#sistem 1

on_message_sensor1 = on_message_mqtt('Soil Moisture Sensor')
on_message_sensor2 = on_message_mqtt('Temperature Sensor')
on_message_sensor3 = on_message_mqtt('Light Level Sensor')

client = mqtt.Client()

#=============================================================================================

#sistem 1
client.message_callback_add('sfarm/moisture', on_message_sensor1)
client.message_callback_add('sfarm/temp', on_message_sensor2)
client.message_callback_add('sfarm/light', on_message_sensor3)

client.on_connect = on_connect

client.connect(settings.MQTT_HOST, settings.MQTT_PORT)
