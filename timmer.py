from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your ChromeDriver
# mine was D:\\Users\\********\\wpi\\A24\\MQP\\Timmer\\chromedriver-win64\\chromedriver.exe
CHROMEDRIVER_PATH = '/path/to/chromedriver'

# URL of the site to be tested
SITE_URL = 'https://example.com'

def measure_site_load_time(url):
    """
    Measures the time it takes for a website to fully load.

    Args:
        url (str): The URL of the website to test.

    Returns:
        float: Load time in milliseconds.
    """
    # Configure Chrome options
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Initialize WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Record start time
        start_time = time.time()

        # Load the site
        driver.get(url)

        # Wait for the page to be fully loaded (example: waiting for body element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Record end time
        end_time = time.time()

        # Calculate load time in milliseconds
        load_time_ms = (end_time - start_time) * 1000
        return load_time_ms

    finally:
        # Quit the driver
        driver.quit()

if __name__ == '__main__':
    try:
        load_time = measure_site_load_time(SITE_URL)
        print(f"Site '{SITE_URL}' loaded in {load_time:.2f} milliseconds.")
    except Exception as e:
        print(f"An error occurred: {e}")
