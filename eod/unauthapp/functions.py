import smtplib
from datetime import datetime

def send_mail(receiver_email, message):
    try:
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login("eodteamhelper@gmail.com", "qpalzmqp")

        # sending the mail
        s.sendmail("sender_email_id", receiver_email, message)

        # terminating the session
        s.quit()
        return True
    except:
        return False

def get_secret_number(string):
    lst = list()
    for i in string:
        lst.append(str(ord(i)))
    return "".join(lst)

def check_secret_number(string, number):
    lst = list()
    for i in string:
        lst.append(str(ord(i)))
    x = "".join(lst)
    return int(x) == int(number)

def email_anonymizer(email):
    str = email.split("@")
    string = str[0]
    s = len(string)
    s = s-3
    x_str = ["*" for i in range(s)]
    x_str = "".join(x_str)
    return string[0:2] + x_str +string[-1]+str[-1]

def active_token(token_time):
    x = int(datetime.timestamp(datetime.now())) - int(token_time)
    return x < 86400
