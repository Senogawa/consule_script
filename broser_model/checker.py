from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

import time
from loader import user_data
from broser_model.auth_module import authorization
from broser_model.auth_module import get_token
from email_module.mail_sender import send_email

def check_info(broser: webdriver.Firefox):
    """
    Заполняет формы и проверяет на наличие расписания
    """

    def find_xpath(broser: webdriver.Chrome, xpath: str, sleep_time: int = 5):
        """
        Нажатие на элемент и ожидание прогрузки
        """

        broser.find_element(By.XPATH, xpath).click()
        time.sleep(sleep_time)

    if broser == "Not valide":
        print("|INFO| Next try through 3 hours |INFO|")
        return

    time.sleep(10)
    broser.find_element(By.CSS_SELECTOR, "#j_id0\:SiteTemplate\:j_id52\:j_id53\:j_id54\:j_id58 > a:nth-child(2)").click()
    time.sleep(7)
    find_xpath(broser, "//input[@value='Nonimmigrant Visa']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Step 1 was finished |INFO|")

    find_xpath(broser, "//input[@value='a0I8a00000rvpr6EAA']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Step 3 was finished |INFO|")

    find_xpath(broser, "//input[@value='a0AC000000ILpJwMAL']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Visa class was selected |INFO|")

    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Step 5 was finished |INFO|")

    find_xpath(broser, "//input[@class='continue nav ui-button ui-widget ui-state-default ui-corner-all']", 7)
    print("|INFO| Step 6 was finished |INFO|")

    find_xpath(broser, "//input[@value='No']", 7)
    print("|INFO| Step 7 was finished |INFO|")

    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Colombo was finished |INFO|")

    broser.find_element(By.CLASS_NAME, "ui-dialog-buttonset").click()
    time.sleep(0.5)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("|INFO| Step 8 was finished |INFO|")
    
    check_counts = 0
    while True:
        if check_counts == 3:
            print("|INFO| Cannot take info |INFO|")
            broser.quit()
            return
        captcha = get_token(broser.current_url, "8dcc6f44-097e-4720-83f1-a87f7ad8e756")
        broser.execute_script("document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML= " + "'" + captcha + "'")
        time.sleep(2)#debug
        find_xpath(broser, "//input[@value='Submit']", 7)

        try:
            broser.switch_to.frame(broser.find_element(By.XPATH, "//iframe[@title='widget containing checkbox for hCaptcha security challenge']"))
        except exceptions.NoSuchElementException:
            break

        if "I am human" in broser.page_source:
            broser.switch_to.default_content()
            check_counts += 1
            continue
        
    broser.switch_to.default_content()        
    if "There are currently no appointments available." not in broser.page_source:
        print("|INFO| New schedule |INFO|")
        send_email()
    else:
        print("|INFO| no schedule |INFO|")
        broser.quit()



if __name__ == "__main__":
    a = authorization(user_data["username"], user_data["password"])
    check_info(a)