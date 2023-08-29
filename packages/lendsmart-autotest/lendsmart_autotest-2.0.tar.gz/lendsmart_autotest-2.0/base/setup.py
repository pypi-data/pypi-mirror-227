"""
    setup the driver
"""
# pylint:disable=C0415,E0401,R0903
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from autotest.lib.configurations.common_config import (
    waitTime, chromiumUserAgent
)
import os
import sys
import shutil
sys.path.insert(0, '/opt')
os.environ["PYTHONPATH"] = "/opt"



def loadBrowser(browser_driver):
    print("Loading browser and browser driver")
    BIN_DIR = "/tmp/bin"
    CURR_BIN_DIR = "/opt"

    if not os.path.exists(BIN_DIR):
        print("Creating bin folder in /tmp")
        os.makedirs(BIN_DIR)
    else:
        print("bin folder already exists in /tmp")

    for i in browser_driver:
        if (i not in (os.listdir('/tmp/bin'))):
            print("Copying " + i + " in /tmp/bin")
            currfile = os.path.join(CURR_BIN_DIR, i)
            newfile = os.path.join(BIN_DIR, i)
            shutil.copy2(currfile, newfile)

            print("Giving permissions for lambda")
            os.chmod(newfile, 0o775)

        else:
            print(i + " already present in /tmp/bin")


class DriverSetup:
    """
    Setup the driver
    """

    def get_driver(
        self, browser_type: str, driver_path: str = None, chromium_path: str = None
    ):
        """
        load the driver
        """
        driver = None
        if not driver_path:
            driver_path = "/opt/chromedriver"
        if not chromium_path:
            chromium_path = "/opt/chrome/chrome"
        print("driver path==>", driver_path)

        from urllib3.connectionpool import log as urllibLogger

        urllibLogger.setLevel(logging.INFO)

        if browser_type == "headless-chromium": 
            #loadBrowser(browser_driver=["headless-chromium","chromedriver"])
            options = Options()
            options.binary_location = chromium_path
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(driver_path,chrome_options=options)

        print(driver.get_window_size())
        return driver
