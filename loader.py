from configparser import ConfigParser

cnf = ConfigParser()
cnf.read("cnf.ini")
user_data = cnf["USER"]
mail_data = cnf["EMAIL"]
captcha_data = cnf["CAPTCHA"]

