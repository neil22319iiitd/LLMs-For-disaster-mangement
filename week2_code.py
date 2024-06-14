import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

# Suppress logging messages
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Set Chrome log level to suppress warnings

# Specify the path to the ChromeDriver executable
path = "C:\\webdrivers\\chromedriver.exe"
service = Service(path)

# Initialize the Chrome WebDriver with the service
driver = webdriver.Chrome(service=service, options=options)

# Open Twitter and login
driver.get("https://twitter.com/login")

sleep(4)

username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys("@NeilMehta82875")
next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
next_button.click()

sleep(4)
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys('nei@8447')
log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
log_in.click()

# Wait for the login to complete
sleep(5)

# Navigate to the search page
driver.get("https://twitter.com/search-home")

# Wait for the search page to load
sleep(3)

# List of significant bridges
bridges = [
    "Pampa",
    "Cheruthoni",
    "Aluva",
    "Muthirapuzha",
    "Thodupuzha"
]

# List of significant hospitals
hospitals = [
    "KIMS",
    "Aster Medcity",
    "Amrita Hospital",
    "Lisie Hospital",
    "Rajagiri Hospital"
]

# Data containers for bridges
BridgeUserTags = []
BridgeTimeStamps = []
BridgeTweets = []
BridgeReplys = []
BridgeReTweets = []
BridgeLikes = []

# Perform search for each bridge and collect tweets
for bridge in bridges:
    search_url = (
        f'https://twitter.com/search?q={bridge}%20Bridge%20'
        'until%3A2018-08-25%20since%3A2018-08-07&src=typed_query'
    )
    print(f"Visiting URL: {search_url}")
    driver.get(search_url)
    
    # Give the page time to load the results
    sleep(5)
    
    # Scroll down to load more tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Collect tweets
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        try:
            UserTag = article.find_element(By.XPATH, ".//div[@data-testid='tweet']").get_attribute('textContent')
        except Exception as e:
            logging.error(f"Error extracting User-Tag: {e}")
            UserTag = ""
        BridgeUserTags.append(UserTag)
        
        try:
            TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
        except Exception as e:
            logging.error(f"Error extracting TimeStamp: {e}")
            TimeStamp = ""
        BridgeTimeStamps.append(TimeStamp)
        
        try:
            Tweet = article.find_element(By.XPATH, ".//div[@lang]").text
        except Exception as e:
            logging.error(f"Error extracting Tweet: {e}")
            Tweet = ""
        BridgeTweets.append(Tweet)
        
        try:
            Reply = article.find_element(By.XPATH, ".//button[@data-testid='reply']").text
        except Exception as e:
            logging.error(f"Error extracting Reply: {e}")
            Reply = ""
        BridgeReplys.append(Reply)
        
        try:
            reTweet = article.find_element(By.XPATH, ".//button[@data-testid='retweet']").text
        except Exception as e:
            logging.error(f"Error extracting Retweet: {e}")
            reTweet = ""
        BridgeReTweets.append(reTweet)
        
        try:
            Like = article.find_element(By.XPATH, ".//button[@data-testid='like']").text
        except Exception as e:
            logging.error(f"Error extracting Like: {e}")
            Like = ""
        BridgeLikes.append(Like)
    
    print(f"Total tweets extracted for {bridge}: {len(articles)}")

# Data containers for hospitals
HospitalUserTags = []
HospitalTimeStamps = []
HospitalTweets = []
HospitalReplys = []
HospitalReTweets = []
HospitalLikes = []

# Perform search for each hospital and collect tweets
for hospital in hospitals:
    search_url = (
        f'https://twitter.com/search?q={hospital}%20Hospital%20'
        'until%3A2018-08-25%20since%3A2018-08-07&src=typed_query'
    )
    print(f"Visiting URL: {search_url}")
    driver.get(search_url)
    
    # Give the page time to load the results
    sleep(5)
    
    # Scroll down to load more tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Collect tweets
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        try:
            UserTag = article.find_element(By.XPATH, ".//div[@data-testid='tweet']").get_attribute('textContent')
        except Exception as e:
            logging.error(f"Error extracting User-Tag: {e}")
            UserTag = ""
        HospitalUserTags.append(UserTag)
        
        try:
            TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
        except Exception as e:
            logging.error(f"Error extracting TimeStamp: {e}")
            TimeStamp = ""
        HospitalTimeStamps.append(TimeStamp)
        
        try:
            Tweet = article.find_element(By.XPATH, ".//div[@lang]").text
        except Exception as e:
            logging.error(f"Error extracting Tweet: {e}")
            Tweet = ""
        HospitalTweets.append(Tweet)
        
        try:
            Reply = article.find_element(By.XPATH, ".//button[@data-testid='reply']").text
        except Exception as e:
            logging.error(f"Error extracting Reply: {e}")
            Reply = ""
        HospitalReplys.append(Reply)
        
        try:
            reTweet = article.find_element(By.XPATH, ".//button[@data-testid='retweet']").text
        except Exception as e:
            logging.error(f"Error extracting Retweet: {e}")
            reTweet = ""
        HospitalReTweets.append(reTweet)
        
        try:
            Like = article.find_element(By.XPATH, ".//button[@data-testid='like']").text
        except Exception as e:
            logging.error(f"Error extracting Like: {e}")
            Like = ""
        HospitalLikes.append(Like)
    
    print(f"Total tweets extracted for {hospital}: {len(articles)}")

# Close the WebDriver
driver.quit()

# Create DataFrames
bridge_df = pd.DataFrame({
    'UserTags': BridgeUserTags,
    'TimeStamps': BridgeTimeStamps,
    'Tweets': BridgeTweets,
    'Replys': BridgeReplys,
    'reTweets': BridgeReTweets,
    'Likes': BridgeLikes
})

hospital_df = pd.DataFrame({
    'UserTags': HospitalUserTags,
    'TimeStamps': HospitalTimeStamps,
    'Tweets': HospitalTweets,
    'Replys': HospitalReplys,
    'reTweets': HospitalReTweets,
    'Likes': HospitalLikes
})

# Save tweets to Excel files
bridge_excel_file = "kerala_bridges.xlsx"
hospital_excel_file = "kerala_hospitals.xlsx"
bridge_df.to_excel(bridge_excel_file, index=False)
hospital_df.to_excel(hospital_excel_file, index=False)

print(f"Total number of bridge tweets extracted: {len(bridge_df)}")
print(f"Bridge Excel file saved: {bridge_excel_file}")
print(f"Total number of hospital tweets extracted: {len(hospital_df)}")
print(f"Hospital Excel file saved: {hospital_excel_file}")
