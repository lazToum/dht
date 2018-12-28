# DHT
Python script that reads humidity and temperature (from a DHT11 | DHT22 | AM2302 sensor) and publishes these values to a mqtt broker.

Libraries used ([requirements.txt](./requirements.txt)):

- Adafruit-DHT
- paho-mqtt
- PyJWT
- python-dotenv

Specify in [dht.env](./dht.env):
```
DHT_PIN=4  # the pin number the sensor is connected to the raspberry pi
DHT_SENSOR=11  # 11: Adafruit_DHT.DHT11, 22: Adafruit_DHT.DHT22, 2302: Adafruit_DHT.AM2302 
WAIT_INTERVAL=2  # the number seconds to wait before reading and publishing the values 
SUBMISSIONS_LIMIT=-1  # the number of valuesto read and publish (-1: no limit)
ERRORS_LIMIT=-1  # the number of errors to allow before exitting
MQTT_BROKER="iot.eclipse.org"  # the hostname (or ip) of the mqtt broker
MQTT_PORT=1883  # the port the mqtt broker is listening
JWT_SECRET="secret" # the jwt secret to use (if needed: https://github.com/emqx/emqx-auth-jwt) 
MQTT_USER="pi" # the user to authenticate for the mqtt connection
MQTT_TOPIC="/raspberry/dht/data/" # the topic to publish the values
```

Use the [Makefile](./Makefile) to create /usr/local/bin/dht\
(or custom prefix/bin/dht) and create a systemd service.

`systemctl start|stop|status|enable|disable dht.service`
