import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883, 60)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        data = {
            'tempc': round(temperature,1),
            'hum': round(humidity),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        client.publish("devices/sensors/weather_IoTLab", json.dumps(data))
        print(json.dumps(data))
        client.publish("devices/sensors/temp_IoTLab", round(temperature,1))
        client.publish("devices/sensors/hum_IoTLab", round(humidity))
    else:
        print("Failed to retrieve data from sensor")
    time.sleep(30)
