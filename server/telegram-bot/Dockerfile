FROM python:3.8

ADD telegram-bot.py /
ADD secrets /
ADD subscribers /
ADD requirements.txt /

RUN pip install -r requirements.txt
CMD [ "python", "-u", "./telegram-bot.py" ]