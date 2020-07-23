SET ALARM_CONTAINER_TAG=alarm-bot-telegram
docker build -t %ALARM_CONTAINER_TAG% .
docker run %ALARM_CONTAINER_TAG%