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

# Path to your MITMProxy's CA certificate
CA_CERTIFICATE_PATH = 'mitmproxy-ca-cert.crt'

# URL of the site to be tested
SITE_URL = 'https://login.microsoftonline.com'

# Output file for results
OUTPUT_FILE = sys.argv[1]

NUM_REQUESTS = 50

# Clear the output file
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
    options.add_argument('--ignore-certificate-errors')  # Ignore certificate errors
    options.add_argument('--ignore-ssl-errors')         # Ignore SSL errors
    options.add_argument('--allow-insecure-localhost')  # Allow localhost access
    options.add_argument('--user-data-dir=C:\\Temp\\chrome_user_data')  # Temp data folder
    options.add_argument('--disk-cache-dir=C:\\Temp\\chrome_cache')  # Cache folder
    options.add_argument('--disable-dev-shm-usage')  # Use /tmp instead of /dev/shm
    options.add_argument('--disable-extensions')  # Disable Chrome extensions
    options.add_argument('--disable-background-networking')  # Disable background tasks
    options.add_argument('--disable-sync')  # Disable Chrome Sync
    options.add_argument('--disable-default-apps')  # Disable default apps

    # Initialize WebDriver with detailed logging
    service = Service(CHROMEDRIVER_PATH)
    service.log_path = "chromedriver.log"  # Log ChromeDriver output

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
            time.sleep(2)  # Add a delay between requests to reduce resource contention
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
