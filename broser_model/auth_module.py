from socket import timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from python3_anticaptcha import HCaptchaTaskProxyless
from fake_useragent import UserAgent

from loader import user_data
from loader import captcha_data


def get_token(url: str, site: str) -> str:
    """
    Получение токена капчи
    """
    while True:
        api = captcha_data["api_key"]
        result = HCaptchaTaskProxyless.HCaptchaTaskProxyless(anticaptcha_key=api).captcha_handler(websiteURL=url, websiteKey=site)
        if "errorCode" in result.keys():
            print("No workers")
            continue
        else:
            break
    print("Captcha solved")
    return result["solution"]["gRecaptchaResponse"]


def authorization(username: str, password: str) -> webdriver.Firefox:
    """
    Аутентификация аккаунта
    Возвращает браузер, для функции checker.check_info
    """
    try_counts = 0
    while True:
        if try_counts == 4:
            print("|INFO| Authorization captcha not valide |INFO|")
            broser.quit()
            return "Not valide"

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent().random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        broser = webdriver.Chrome(executable_path = "./chromedriver", options = options)
        
        broser.get("https://cgifederal.secure.force.com/")

        broser.find_element(By.XPATH,"//input[@id='loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username']").send_keys(username)
        broser.find_element(By.XPATH,"//input[@id='loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password']").send_keys(password)
        broser.find_element(By.XPATH,"//input[@type='checkbox']").click()

        code = get_token("https://cgifederal.secure.force.com/","8dcc6f44-097e-4720-83f1-a87f7ad8e756")
        broser.execute_script("document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML= " + "'" + code + "'")
        print("captcha inputed")
        time.sleep(2) #debug
        broser.find_element(By.XPATH, "//input[@id='loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton']").click()
        time.sleep(2)
        if "Error" not in broser.page_source:
            return broser
        else:
            print("|INFO| Not valide captcha |INFO|")
            try_counts += 1
            broser.quit()
    


if __name__ == "__main__":
    authorization(user_data["username"], user_data["password"])
   