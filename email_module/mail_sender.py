import smtplib
from email.mime.text import MIMEText
import requests

from loader import mail_data
from loader import bot_data
from datetime import datetime




def send_email(subject: str ,message: str):
    """
    Модуль для отправки сообщения на почту
    |INFO| Настройка почты происходит в конфигурационном файле cnf.ini |INFO|
    """
    mail_sendler = smtplib.SMTP("smtp.gmail.com", 587)
    mail_sendler.starttls()
    msg = MIMEText(message)
    msg["Subject"] = subject
    mail_sendler.login(mail_data["from_mail"], mail_data["from_mail_password"])
    mail_sendler.sendmail(mail_data["from_mail"], mail_data["to_mail"], msg.as_string())
    mail_sendler.quit()

def send_telegram_message(text: str):
    requests.get(f"https://api.telegram.org/bot{bot_data['token']}/sendMessage?chat_id={bot_data['chat_id']}&text={text}")

if __name__ == "__main__":
    #send_telegram_message("| INFO | Начинаю работу | INFO |")
    #send_telegram_message("Посольство: Расписание встреч\nНа сайте появились рассписания встреч\nПроверьте сайт")
    send_telegram_message(f"Уведомление о работе\nПродолжаю работу\n{datetime.now().strftime('%H-%M-%S : %d-%m-%Y')}")