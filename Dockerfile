FROM python:3.8

ADD src/alarm.py /

RUN pip install gpiozero
CMD [ "python", "./alarm.py" ]