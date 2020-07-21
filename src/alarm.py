import pathlib
import time

from gpiozero import Button

from src.log_lib import log_message

from datetime import date

# # CONFIGURATION   #

# pin configuration

GPIO_X = 27     # alarm
GPIO_Y = 4      # reed
GPIO_Z = 17     # tamper

# directory configuration

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

# timing configuration

TICKING_TIME = 1  # seconds

# setup

# we can treat sensor switches as GPIO Buttons
alarm = Button(GPIO_X)
reed = Button(GPIO_Y)
tamper = Button(GPIO_Z)

# loop forever
while True:

    # remember that the sensor is NC (Normally Closed), so if the switch is closed, it's all ok.
    if not alarm.is_pressed:
        log_message("Alarm triggered")
        # TODO: communicate this event on the asynchronous channel

    if not reed.is_pressed:
        log_message("Reed triggered")
        # TODO: communicate this event on the asynchronous channel

    if not tamper.is_pressed:
        log_message("Tamper triggered")
        # TODO: communicate this event on the asynchronous channel

    time.sleep(TICKING_TIME)