from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from write_log import write_log
from write_log import write_log
from time import sleep
from shutil import rmtree
from os.path import exists
from verify_identity import verify_identity


def driver_start(email, url):
    write_log("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    if exists(f"accounts/{email}/cache2"):
        rmtree(f"accounts/{email}/cache2")

    try:
        service = Service("driver/geckodriver")
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("-profile")
        options.add_argument(f"accounts/{email}")
        # options.headless = True

        driver = Firefox(service=service, options=options)
        driver.get(url)
        driver.maximize_window()
        driver.set_page_load_timeout(30)
        sleep(4)

        if driver.current_url.startswith(url):
            pass
        elif driver.current_url.startswith("https://accounts.google.com/signin"):
            verify_identity(email, driver)
            sleep(4)

    except Exception as e:
        write_log(f"ERROR : Could not log in: ({email}) \n{str(e)}")
        driver.close()
    else:
        write_log(f"OK : Session started ({email})")

    return driver
