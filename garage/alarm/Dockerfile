FROM python:3.8

ADD alarm.py /
ADD log_lib.py /
ADD mqttpublish.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
CMD [ "python", "-u", "./alarm.py" ]