import schedule
import sys
print(sys.path)

from broser_model.checker import check_info
from broser_model.auth_module import authorization
from loader import user_data


def check_all_info():
    broser = authorization(user_data["username"], user_data["password"])
    check_info(broser)

def main():
    schedule.every(1).seconds.do(check_all_info)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()
