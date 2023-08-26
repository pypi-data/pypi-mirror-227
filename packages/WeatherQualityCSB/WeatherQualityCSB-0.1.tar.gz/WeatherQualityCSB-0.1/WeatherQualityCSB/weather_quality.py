import pytest
import os
import sys
import time
import json
import logging
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .validations import validate_locations, validate_date, validate_params

logging.basicConfig(level=logging.INFO)


class WeatherQuality:
    """
    A utility class to fetch weather quality data from the CSB website and save it as an Excel file.

    Attributes:
    -----------
    locations: dict
        A dictionary where the keys represent the city names and the values are lists of district names.
        If locations is an empty dictionary or if a city's list of districts is empty, data for all cities/districts
        will be fetched.
    dates: tuple
        A tuple containing the start and end dates in the format (start_date, end_date).
    params: list, optional
        A list of parameters to select when fetching data. If this is empty or None, data for all parameters will
        be fetched.
    headless: bool, optional
        Determines if the browser runs in headless mode (i.e., no GUI).
    download_path: str, optional
        Path to the directory where the Excel file will be downloaded.
    logs: bool, optional
        Determines if progress logs should be printed to the console.
    """

    class WebDriverManager:
        """
        Manages the selenium webdriver, including setup and teardown of the browser.

        Attributes:
        -----------
        BASE_URL: str
            The base URL of the CSB website.
        WAIT_TIME: int
            Implicit wait time for the webdriver in seconds.
        WINDOW_SIZE: tuple
            Desired window size for the webdriver.
        driver: webdriver.Chrome
            The selenium Chrome webdriver instance.
        """
        BASE_URL = "https://sim.csb.gov.tr/STN/STN_Report/StationDataDownloadNew"
        WAIT_TIME = 30
        WINDOW_SIZE = (1366, 728)

        def __init__(self, options):
            """
            Initialize the WebDriverManager with the provided options.

            Parameters:
            -----------
            options: webdriver.ChromeOptions
                Chrome options for selenium webdriver.
            """
            self.driver = webdriver.Chrome(options=options)
            self.setup()

        def setup(self):
            """
            Sets up the webdriver by opening the BASE_URL and setting the desired window size and wait time.
            """
            self.driver.get(self.BASE_URL)
            self.driver.set_window_size(*self.WINDOW_SIZE)
            self.driver.implicitly_wait(self.WAIT_TIME)
            time.sleep(3)

        def teardown(self):
            """
            Quits the webdriver, closing all associated browser windows.
            """
            self.driver.quit()

    def __init__(self, locations, dates, params=None, headless=False, download_path=None, logs=True):
        """
        Initialize the WeatherQuality instance.

        Parameters:
        -----------
        locations: dict
            Dictionary of city names and associated districts to fetch data for.
        dates: tuple
            Start and end dates in the format (start_date, end_date) to fetch data for.
        params: list, optional (default: None)
            Parameters to select when fetching data.
        headless: bool, optional (default: False)
            Whether to run the browser in headless mode.
        download_path: str, optional
            Path where the Excel file will be downloaded. Default is the user's Downloads directory.
        logs: bool, optional (default: True)
            Whether to print progress logs to the console.
        """
        self.locations = locations
        self.districts = [district for districts in locations.values() for district in districts]
        self.startDate, self.endDate = dates
        self.params = params
        self.logs = logs

        self.download_path = download_path or self._default_download_path()
        self.downloaded_file_path = None
        self.options = self._setup_webdriver_options(headless)
        self.initial_files = set(os.listdir(self.download_path))
        self.web_manager = self.WebDriverManager(self.options)

        self.__validate()

    def _setup_webdriver_options(self, headless):
        """
        Sets up the Chrome webdriver options.

        Parameters:
        ----------
        headless: bool
            Whether to run the browser in headless mode.
        Returns:
        --------
        options: webdriver.ChromeOptions
            Chrome options for selenium webdriver.
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "download.default_directory": self.download_path
        }
        options.add_experimental_option("prefs", prefs)
        return options

    @staticmethod
    def _default_download_path():
        """
        Determines the default download path based on the OS.

        Returns:
        --------
        str:
            The path to the default download directory.
        """
        return os.path.join(os.path.expanduser('~'), 'Downloads') if os.name != 'nt' else os.path.join(
            os.environ['USERPROFILE'], 'Downloads')

    def __validate(self):
        """
        Validates locations, dates, and parameters using utility functions.
        """
        validate_locations(self.locations)
        validate_date([self.startDate, self.endDate])
        validate_params(self.params)

    def run(self):
        """
        Initiates the process to fetch weather quality data from the CSB website and download it as an Excel file.
        """
        if self.logs:
            logging.info("-" * 50)
            logging.info("EXECUTION STARTED")
            logging.info("-" * 50)

        tasks = [
            ("Selecting cities", self.__select_cities),
            ("Selecting districts", self.__select_district),
            ("Selecting parameters", self.__select_params),
            ("Selecting dates", self.__select_dates),
            ("Fetching excel", self.__fetch_excel),
            ("Waiting for file download", self.__wait_for_file_download)
        ]

        try:
            self._execute_tasks(tasks)
        except TimeoutError:
            logging.error("File download timeout reached. Exiting.")
            sys.exit(1)
        finally:
            self.web_manager.teardown()
            if self.logs:
                logging.info("-" * 50)
                logging.info("Browser closed. Successfully completed.")
                logging.info("-" * 50)

    def _execute_tasks(self, tasks):
        """
        Executes the provided list of tasks sequentially.

        Parameters:
        -----------
        tasks: list of tuple
            A list of tasks where each task is represented as a tuple containing task name and associated function.
        """
        self.progress_bar = tqdm(total=len(tasks), unit="task", file=sys.stderr) if self.logs else None
        try:
            for task_name, task_func in tasks:
                if self.logs:
                    self.progress_bar.set_description(f"Current task: {task_name}")
                task_func()
                if self.logs:
                    self.progress_bar.update(1)
        finally:
            if self.logs:
                self.progress_bar.close()  # Close the progress bar first.

                # Then log the download path.
                if hasattr(self, 'downloaded_file_path') and self.downloaded_file_path:
                    logging.info(f"All tasks completed. File downloaded at {self.downloaded_file_path}")
                else:
                    logging.info("All tasks completed.")

    def __select_cities(self):
        """
        Selects the desired cities on the CSB website.
        """
        element = self.web_manager.driver.find_element(By.XPATH,
                                                       "//form[@id=\'StationDataDownloadForm\']"
                                                       "/fieldset/div/div/div/div[2]/div/div/div/div/input")
        element.click()
        time.sleep(1)
        element = self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-input")
        if not self.locations:
            self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-icon:nth-child(5)").click()
        else:
            for city in self.locations.keys():
                if self.logs:
                    self.progress_bar.desc = f"Selecting city: {city}"
                element.send_keys(city)
                time.sleep(1)
                element.send_keys(Keys.ENTER)
                time.sleep(1)

    def __select_district(self):
        """
        Selects the desired districts on the CSB website.
        """
        element = self.web_manager.driver.find_element(By.XPATH,
                                                       "//form[@id=\'StationDataDownloadForm\']"
                                                       "/fieldset/div/div/div/div[3]/div/div/div/div/input")
        element.click()
        time.sleep(1)
        element = self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-input")
        if not self.districts:
            self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-icon:nth-child(5)").click()
        else:
            for district in self.districts:
                if self.logs:
                    self.progress_bar.desc = f"Selecting district: {district}"
                element.send_keys(district)
                time.sleep(1)
                element.send_keys(Keys.ENTER)
                time.sleep(1)

    def __select_params(self):
        """
        Selects the desired parameters on the CSB website.
        """
        element = self.web_manager.driver.find_element(By.XPATH,
                                                       "//form[@id=\'StationDataDownloadForm\']"
                                                       "/fieldset/div/div/div/div[7]/div/div/div/div")
        element.click()
        time.sleep(1)
        element = self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-input")
        if not self.params:
            self.web_manager.driver.find_element(By.CSS_SELECTOR, ".k-state-hover .k-icon:nth-child(5)").click()
        else:
            for param in self.params:
                element.send_keys(param)
                time.sleep(1)
                element.send_keys(Keys.ENTER)
                time.sleep(1)

    def __select_dates(self):
        """
        Inputs the desired start and end dates on the CSB website.
        """
        # Clear the element and send start date
        element = self.web_manager.driver.find_element(By.ID, "StationDataDownload_StartDateTime")
        time.sleep(1)
        element.clear()
        element.send_keys(self.startDate)
        time.sleep(1)

        # Clear the element and send end date
        element = self.web_manager.driver.find_element(By.ID, "StationDataDownload_EndDateTime")
        time.sleep(1)
        element.clear()
        element.send_keys(self.endDate)
        time.sleep(1)

    def __fetch_excel(self):
        """
        Initiates the data fetching process and clicks on the button to download the Excel file.
        """
        # Click on button to fetch data
        self.web_manager.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        # Wait for the desired element to become clickable, up to a maximum of 40 seconds
        wait = WebDriverWait(self.web_manager.driver, 40)
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "EXCEL\'E AKTAR")))
        element.click()

    def __wait_for_file_download(self):
        """
        Waits for the Excel file to be downloaded to the specified directory, with a timeout.
        """
        time_limit = 120  # seconds, i.e., 2 minutes
        start_time = time.time()

        while True:
            current_files = set(os.listdir(self.download_path))
            new_files = current_files - self.initial_files

            for file in new_files:
                if file.endswith(".xlsx"):  # Assuming Excel extension is .xlsx
                    self.downloaded_file_path = os.path.join(self.download_path, file)
                    return

            if time.time() - start_time > time_limit:
                raise TimeoutError("File download timeout reached.")

            time.sleep(1)
