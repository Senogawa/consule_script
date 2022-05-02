from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

import time
from loader import user_data
from auth_module import authorization
from auth_module import get_token
from mail_sender import send_email

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

    time.sleep(10)
    broser.find_element(By.CSS_SELECTOR, "#j_id0\:SiteTemplate\:j_id52\:j_id53\:j_id54\:j_id58 > a:nth-child(2)").click()
    time.sleep(7)
    # broser.find_element(By.XPATH, "//input[@value='Nonimmigrant Visa']").click() #select visa type
    # broser.find_element(By.XPATH, "//input[@value='Continue']").click()
    find_xpath(broser, "//input[@value='Nonimmigrant Visa']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("Step 1 was finished")
    #time.sleep(7)
    # broser.find_element(By.XPATH, "//input[@value='a0I8a00000rvpr6EAA']").click() #select category
    # broser.find_element(By.XPATH, "//input[@value='Continue']").click()
    find_xpath(broser, "//input[@value='a0I8a00000rvpr6EAA']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("Step 3 was finished")
    #time.sleep(7)
    # broser.find_element(By.XPATH, "//input[@value='a0AC000000ILpJwMAL']").click() #select visa class
    # broser.find_element(By.XPATH, "//input[@value='Continue']").click()
    find_xpath(broser, "//input[@value='a0AC000000ILpJwMAL']", 0)
    find_xpath(broser, "//input[@value='Continue']", 7)
    print("Visa class was selected")
    broser.find_element(By.XPATH, "//input[@value='Continue']").click() # step5 - continue
    time.sleep(7)
    broser.find_element(By.XPATH, "//input[@class='continue nav ui-button ui-widget ui-state-default ui-corner-all']").click() # step6 - continue
    time.sleep(7)
    broser.find_element(By.XPATH, "//input[@value='No']").click() # step7 - no
    time.sleep(7)
    broser.find_element(By.XPATH, "//input[@value='Continue']").click() # Colombo - continue
    time.sleep(7)
    #broser.find_element(By.XPATH, "//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']").click() # step 8 dialogue closing
    broser.find_element(By.CLASS_NAME, "ui-dialog-buttonset").click()
    time.sleep(0.5)
    broser.find_element(By.XPATH, "//input[@value='Continue']").click() # step 8 continue
    time.sleep(7)
    check_counts = 0
    while True:
        if check_counts == 3:
            print("Cannot take info")
            broser.quit()
            return
        captcha = get_token(broser.current_url, "8dcc6f44-097e-4720-83f1-a87f7ad8e756")
        broser.execute_script("document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML= " + "'" + captcha + "'")
        broser.find_element(By.XPATH, "//input[@value='Submit']").click() # captcha submit
        time.sleep(7)
        try:
            broser.switch_to.frame(broser.find_element(By.XPATH, "//iframe[@title='widget containing checkbox for hCaptcha security challenge']"))
        except exceptions.NoSuchElementException:
            break

        if "I am human" in broser.page_source:
            print(True)
            broser.switch_to.default_content()
            check_counts += 1
            continue
        # else:
        #     print(False)
        #     broser.switch_to.default_content
        #     break
        
    broser.switch_to.default_content()        
    if "There are currently no appointments available." not in broser.page_source:
        print("New schedule")
        send_email()
    else:
        print("no schedule")
        broser.quit()



if __name__ == "__main__":
    a = authorization(user_data["username"], user_data["password"])
    check_info(a)