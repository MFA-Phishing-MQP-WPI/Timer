from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Event
import sys

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'D:\\Users\\Jacob Glik\\wpi\\A24\\MQP\\Timmer\\chromedriver-win64\\chromedriver.exe'

# URL of the site to be tested
SITE_URL = 'https://youtube.com'

# Output file for results
OUTPUT_FILE = 'site_load_times.txt'

NUM_REQUESTS = 16
NUM_WORKERS = 2 # Limit the number of simultaneous threads
# MAX_RUNTIME = 30  # Maximum runtime in seconds

# Lock for thread-safe printing
print_lock = Lock()
request_number = 0
stop_event = Event()

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
        global request_number
        with print_lock:
            request_number += 1
            print(f"Request {request_number} started.")

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

def worker(url, index):
    """
    Worker function to measure site load time.

    Args:
        url (str): The URL of the website to test.
        index (int): Index to identify the worker.

    Returns:
        tuple: (index, result) - The index and load time or error.
    """
    if stop_event.is_set():
        return index, "Terminated"
    try:
        result = measure_site_load_time(url)
        return index, result
    except Exception as e:
        return index, f"Error: {e}"

def run_with_timeout(idx_deca):
    results = [None] * NUM_WORKERS
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        future_to_index = {executor.submit(worker, SITE_URL, i): i for i in range(NUM_WORKERS)}

        try:
            for future in as_completed(future_to_index):
                # if time.time() - start_time > MAX_RUNTIME:
                #     stop_event.set()
                #     print("Maximum runtime exceeded. Ignoring remaining threads.")
                #     break

                index = future_to_index[future]
                try:
                    idx, result = future.result()
                    results[idx] = result
                    with print_lock:
                        print(f"Request {idx + idx_deca} completed with result: {result}")
                except Exception as e:
                    results[index] = f"Error: {e}"
                    with print_lock:
                        print(f"Request {index} failed with error: {e}")

        except KeyboardInterrupt:
            stop_event.set()
            print("Execution interrupted by user.")

    return results

if __name__ == '__main__':
    results = []
    for idx_deca in range(0, NUM_REQUESTS, NUM_WORKERS):
        results += run_with_timeout(idx_deca)
        time.sleep(0.5)

    # Write completed results to file
    try:
        with open(OUTPUT_FILE, 'w') as f:
            for result in [r for r in results if r is not None]:
                f.write(f"{result}\n")
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to write results to file: {e}")
        sys.exit(1)

    print("Execution finished. Exiting.")
    exit()
