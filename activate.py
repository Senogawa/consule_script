import schedule
import sys
from datetime import datetime

from broser_model.checker import check_info
from broser_model.auth_module import authorization
from email_module.mail_sender import send_email
from loader import user_data


def working_allert():
    send_email("Уведомление о работе", f"Продолжаю работу\n{datetime.now().strftime('%d-%m-%Y : %H-%M-%S')}")

def check_all_info():
    broser = authorization(user_data["username"], user_data["password"])
    check_info(broser)

def main():
    schedule.every(1).day.do(working_allert)
    schedule.every(4).hours.do(check_all_info)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    working_allert()
