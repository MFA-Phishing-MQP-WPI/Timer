# Timmer

https://googlechromelabs.github.io/chrome-for-testing/#stable

1. Download the Correct ChromeDriver Version

    - Go to the ChromeDriver Downloads page.
    - Download the version of ChromeDriver that matches the version of your Chrome browser. You can find your browser version by navigating to `chrome://settings/help` in Chrome.
    - Update the `CHROMEDRIVER_PATH`

2. Update the `CHROMEDRIVER_PATH` variable in the script to the correct path where the ChromeDriver executable is located on your machine. For example:
    ```python
    CHROMEDRIVER_PATH = '/Users/your_username/Downloads/chromedriver'
    ```

3. Add ChromeDriver to `PATH` (Optional)
    - You can add the ChromeDriver executable to your system's `PATH` environment variable. If you do this, you can leave `CHROMEDRIVER_PATH` blank:
      ```python
      driver = webdriver.Chrome(options=options)
      ```
4. Double Check
   ```bash
   python3 -m pip install --upgrade selenium
   chmod +x /path/to/chromedriver
   ```
