import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from datetime import datetime

def download_webpage(url, filename, excluded_strings):
    chrome_driver_path = '/usr/bin/chromedriver'  # Change this to your chromedriver location
    service = Service(chrome_driver_path)
    service.start()
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    # Finds paragraph
    paragraph_elements = driver.find_elements(By.TAG_NAME, "p")
    
    # Extracts text content from <p> tag and excludes specific strings
    text_content = '\n'.join([element.text for element in paragraph_elements if not any(exclude_str in element.text for exclude_str in excluded_strings)])
    
    with open(filename, 'w') as f:
        f.write(text_content)   # Writes text content to txt file

    driver.quit()

def compare_files(initial_file, new_file, differences_file):
    with open(initial_file, 'r') as f:
        initial_content = f.readlines()
    with open(new_file, 'r') as f:
        new_content = f.readlines()
    
    differences = []
    
    # Find additions
    for line in new_content:
        if line not in initial_content:
            differences.append(f"\nNEW: {line}")
    
    # Find removals
    for line in initial_content:
        if line not in new_content:
            differences.append(f"\nOLD: {line} ")
    
    with open(differences_file, 'w') as f:
        f.write(f"URL: {url}\n")
        f.write(f"Timestamp: {time.strftime('%d/%m/%y %H:%M:%S')}\n")
        f.writelines(differences)

if __name__ == "__main__":
    url = input("Please enter URL of the webpage you wish to scrape: ") # user input
    print("\nPress CTRL+C to cancel webscraping")
    output_dir = "webpages"
    os.makedirs(output_dir, exist_ok=True)
    
    # Excluded strings for RTE
    excluded_strings = [
        "We need your consent to load this comcast-player content",
        "We use comcast-player to manage extra content that can set cookies on your device and collect data about your activity. Please review their details and accept them to load the content.Manage Preferences",
        "Use precise geolocation data. Actively scan device characteristics for identification. Store and/or access information on a device. Develop and improve services. Measure content performance. Understand audiences through statistics or combinations of data from different sources. Use limited data to select advertising. Create profiles for personalised advertising. Use profiles to select personalised advertising. Create profiles to personalise content. Use profiles to select personalised content. Measure advertising performance. Use limited data to select content.",
        "List of Partners (vendors)"
    ]
    
    initial_file = os.path.join(output_dir, "initial.txt")
    download_webpage(url, initial_file, excluded_strings)
    latest_file = initial_file
    
    while True:
        new_file = os.path.join(output_dir, "new.txt")
        download_webpage(url, new_file, excluded_strings)
        
        differences_file = os.path.join(output_dir, "differences.txt")
        compare_files(initial_file, new_file, differences_file)
        
        # Rewrites to newest file
        os.replace(new_file, latest_file)
        latest_file = new_file
        
        time.sleep(30)

# The following resources aided with research and development of the code above
# https://github.com/gigafide/basic_python_scraping
# https://blog.finxter.com/5-best-ways-to-write-a-text-file-in-selenium-with-python/
