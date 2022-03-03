from datetime import datetime


def log_message(message):
    today = datetime.now()
    log_file = open(today.strftime("%d-%m-%Y") + '.log', 'a+')  # append or create and append
    message = "[ " + today.strftime("%H:%M:%S") + " ] " + message
    print(message)
    log_file.write(message)
    log_file.close()
