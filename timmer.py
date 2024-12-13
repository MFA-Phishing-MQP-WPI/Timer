from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

if len(sys.argv) != 2:
    print("> ! Required arg missing.")
    print("Usage: python3 timmer.py <NAME_OF_OUTPUT_FILE>")
    exit()

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'chromedriver-win64\\chromedriver.exe'

# URL of the site to be tested
SITE_URL = 'https://google.com'

# Output file for results
OUTPUT_FILE = sys.argv[1]# 'site_load_times.txt'

NUM_REQUESTS = 40

open(OUTPUT_FILE, 'w').write('')

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
        print(f"Request started.")

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
    results = []

    for i in range(NUM_REQUESTS):
        try:
            result = measure_site_load_time(SITE_URL)
            results.append(result)
            print(f"Request {i} completed with result: {result}")
            open(OUTPUT_FILE, 'a').write(f'{result}\n')
        except Exception as e:
            results.append(f"Error: {e}")
            print(f"Request {i} failed with error: {e}")

    # Write completed results to file
    try:
        with open(OUTPUT_FILE, 'w') as f:
            for result in results:
                f.write(f"{result}\n")
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to write results to file: {e}")
        sys.exit(1)

    print("Execution finished. Exiting.")
