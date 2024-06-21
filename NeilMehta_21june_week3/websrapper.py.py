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
username.send_keys("@NeilMehta180745")
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

# Read keywords from text file
with open("keywords19.txt", "r") as file:
    keywords = [line.strip() for line in file]

# Data containers
UserTags = []
TimeStamps = []
Tweets = []
Replys = []
ReTweets = []
Likes = []

# Perform search for each keyword and collect tweets
for i in range(1,2):
    search_query = f'Kerala flood 2018'
    search_url = (
        f'https://twitter.com/search?q={search_query}&src=typed_query'
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
        UserTags.append(UserTag)
        
        try:
            TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
        except Exception as e:
            logging.error(f"Error extracting TimeStamp: {e}")
            TimeStamp = ""
        TimeStamps.append(TimeStamp)
        
        try:
            Tweet = article.find_element(By.XPATH, ".//div[@lang]").text
        except Exception as e:
            logging.error(f"Error extracting Tweet: {e}")
            Tweet = ""
        Tweets.append(Tweet)
        
        try:
            Reply = article.find_element(By.XPATH, ".//button[@data-testid='reply']").text
        except Exception as e:
            logging.error(f"Error extracting Reply: {e}")
            Reply = ""
        Replys.append(Reply)
        
        try:
            reTweet = article.find_element(By.XPATH, ".//button[@data-testid='retweet']").text
        except Exception as e:
            logging.error(f"Error extracting Retweet: {e}")
            reTweet = ""
        ReTweets.append(reTweet)
        
        try:
            Like = article.find_element(By.XPATH, ".//button[@data-testid='like']").text
        except Exception as e:
            logging.error(f"Error extracting Like: {e}")
            Like = ""
        Likes.append(Like)
    
    print(f"Total tweets extracted for keyword 'hello': {len(articles)}")

# Close the WebDriver
driver.quit()

# Create DataFrame
tweets_df = pd.DataFrame({
    'UserTags': UserTags,
    'TimeStamps': TimeStamps,
    'Tweets': Tweets,
    'Replys': Replys,
    'ReTweets': ReTweets,
    'Likes': Likes
})

# Save tweets to CSV file
csv_file = "kerala_floods_2018_tweets20.csv"
tweets_df.to_csv(csv_file, index=False)

print(f"Total number of tweets extracted: {len(tweets_df)}")
print(f"CSV file saved: {csv_file}")
