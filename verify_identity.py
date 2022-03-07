from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from write_log import write_log
from time import sleep


def verify_identity(email, driver):

    heading_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "headingText"))
            ).text
    write_log(heading_text)

    if heading_text == "Verify it’s you" or heading_text == "Verify that it’s you":
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
        form.find_element(
            By.TAG_NAME, "ol"
            ).find_element(
                By.TAG_NAME, "li"
                ).click()
                
    else:

        try:
            with open("_accounts.txt") as f:
                lines = f.readlines()

            for line in lines:
                if line.split(":")[0] == email:
                    password = line.split(":")[1]

            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-vQzf8d"))
                )
            next_button.click()

            sleep(2)
            
            password_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
                )
            )
            password_field.send_keys(password)
            sleep(.2)
            password_field.send_keys(Keys.ENTER)
        
        except Exception as e:
            write_log([f"ERROR : login_verify_identity ({email}) ; {str(e)}"])

        else:
            write_log([f"OK : login_verify_identity ({email})"])
