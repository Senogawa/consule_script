import smtplib
from email.mime.text import MIMEText
from loader import mail_data




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

if __name__ == "__main__":
    send_email("Посольство: Расписание встреч", "На сайте появились рассписания встреч \n Проверьте сайт")