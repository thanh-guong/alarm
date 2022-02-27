FROM python:3.8

ADD producer-proxy.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
CMD [ "python", "-u", "./producer-proxy.py" ]