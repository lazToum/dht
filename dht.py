#!/usr/bin/env python3
import os
import sys
import time
import Adafruit_DHT
import paho.mqtt.publish as publish
import jwt
import json
import logging
from datetime import datetime
from dotenv import load_dotenv


logging.basicConfig(level="INFO")
DOT_ENV_PATH = os.getenv('PREFIX', '/usr/local/share/dht.env')
if os.path.exists(DOT_ENV_PATH):
    load_dotenv(dotenv_path=DOT_ENV_PATH)

# number of seconds to wait on each loop
WAIT_INTERVAL = int(os.getenv('WAIT_INTERVAL', 2))
# maximum number of values to publish ( -1: no limit)
SUBMISSIONS_LIMIT = int(os.getenv('SUBMISSIONS_LIMIT', -1))
# maximum number of errors to accept before quitting (-1: no limit)
ERRORS_LIMIT = int(os.getenv('ERRORS_LIMIT', -1))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', '/raspberry/dht/data/')
# the hostname (or ip) of the mqtt broker
MQTT_BROKER = os.getenv('MQTT_BROKER', 'iot.eclipse.org')
# the port of the mqqtt broker
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
# the jwt secret to encode for authenticating with emqx
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')
# the user to authenticating to the broker (empty:  no authentication)
MQTT_USER = os.getenv('MQTT_USER', '')
# the password to authenticating to the broker
# (empty: jwt encode with the jwt secret, for emqx jwt.auth)
_mqtt_password = os.getenv('MQTT_PASSWORD', '')
MQTT_PASSWORD = _mqtt_password if (_mqtt_password != '' and MQTT_USER != '') else jwt.encode(
    {'sensors': ['temperature', 'humidity']},
    JWT_SECRET,
    algorithm='HS256'
)

# the dht sensor to use (DHT11, DHT22, AM2302)
DHT_SENSOR = int(os.getenv('DHT_SENSOR', Adafruit_DHT.DHT11))
# the data pin (on the board) of the dht sensor
DHT_PIN = int(os.getenv('DHT_PIN', 4))

errors_count = 0
submissions = 0
while True and not (
        (0 < ERRORS_LIMIT <= errors_count) or
        (0 < SUBMISSIONS_LIMIT <= submissions)):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            try:
                _now = datetime.now()
                publish.single(
                    topic=MQTT_TOPIC,
                    payload=json.dumps(
                        {
                            'datetime': _now,
                            'temperature': temperature,
                            'humidity': humidity
                        },
                        default=str
                    ),
                    port=MQTT_PORT,
                    hostname=MQTT_BROKER,
                    auth={
                        'username': MQTT_USER, 'password': MQTT_PASSWORD
                    } if MQTT_USER != '' else None)
                logging.info(
                    'Temp={0:0.1f}*C, Humidity={1:0.1f}%, Datetime={2}'
                    .format(
                        temperature,
                        humidity,
                        _now.isoformat(' ')
                    )
                )
                errors_count = 0
                submissions += 1
            except Exception as e:
                logging.warning(e)
                errors_count += 1
        else:
            errors_count += 1
            logging.warning('Failed to read from the sensor!')
        time.sleep(WAIT_INTERVAL)
    except KeyboardInterrupt:
        logging.warning(' Got KeyboardInterrupt ... stopping')
        sys.exit(0)

sys.exit(int(errors_count >= ERRORS_LIMIT))
