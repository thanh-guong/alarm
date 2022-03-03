import pathlib
import time

from gpiozero import Button
from log_lib import log_message
from mqttpublish import publish_alarm_status

# # CONFIGURATION   #

# pin configuration

GPIO_X = 27     # alarm
GPIO_Y = 4      # reed
GPIO_Z = 17     # tamper

# directory configuration

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

# timing configuration

TICKING_TIME = 1            # seconds
ONLINE_TICKING_TIME = 9     # seconds (15 min)

# setup

# we can treat sensor switches as GPIO Buttons
alarm = Button(GPIO_X)
reed = Button(GPIO_Y)
tamper = Button(GPIO_Z)

online_counter = 0

# loop forever
while True:

    # remember that the sensor is NC (Normally Closed), so if the switch is closed, it's all ok.
    if not alarm.is_pressed:
        log_message("Alarm triggered")
        publish_alarm_status("alarm")

    if not reed.is_pressed:
        log_message("Reed triggered")
        publish_alarm_status("reed")

    if not tamper.is_pressed:
        log_message("Tamper triggered")
        publish_alarm_status("tamper")

    if online_counter == ONLINE_TICKING_TIME:
        log_message("Sending online message")
        publish_alarm_status("online")
        online_counter = 0

    time.sleep(TICKING_TIME)
    online_counter += 1
