from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
from write_log import write_log
from os import mkdir
from shutil import rmtree


def login(email, password):
    service = Service("driver/geckodriver")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("-profile")
    mkdir(f"accounts/{email}")
    options.add_argument(f"accounts/{email}")
    # options.headless = True

    driver = Firefox(service=service, options=options)
    driver.get(f"https://accounts.google.com/signin/v2/identifier?Email={email}")
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    sleep(3)

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-vQzf8d"))
    )
    next_button.click()

    try:
        incorrect_email_message = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".o6cuMc"))
        )
    except:
        pass
    else:
        write_log([f"ERROR : Incorrect email ({email})"])
        driver.close()

    sleep(2)
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        )
    )
    password_field.send_keys(password)
    sleep(.2)
    password_field.send_keys(Keys.ENTER)

    try:
        incorrect_password_message = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".OyEIQ > div:nth-child(2)"))
    )
    except:
        pass
    else: 
        write_log([f"ERROR : Incorrect password ({email})"])
        driver.close()

    driver.close()


def credentials_validate(email, password):
    try:
        login(email, password)

        with open("accounts.txt", "a") as f:
            f.write(f"{email}:{password}\n")

        with open("accounts.txt", "r") as f:
            f.read(f"{email}:{password}\n")
            
    except:
        write_log([f"ERROR : Login ({email})"])
        rmtree(
            f"accounts/{email}",)

    else:
        write_log(f"NEW ACC : {email}")
