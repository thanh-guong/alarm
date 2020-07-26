FROM python:3.8

ADD consumer-proxy.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
CMD [ "python", "./consumer-proxy.py" ]