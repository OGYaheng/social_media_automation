import tweepy
import facebook
import schedule
import time
import logging
from datetime import datetime

logging.basicConfig(filename="social_media_automation.log", level=logging.INFO)

# Twitter API 認證
twitter_consumer_key = 'your_twitter_consumer_key'
twitter_consumer_secret = 'your_twitter_consumer_secret'
twitter_access_token = 'your_twitter_access_token'
twitter_access_token_secret = 'your_twitter_access_token_secret'

# Facebook API 認證
facebook_access_token = 'your_facebook_access_token'
facebook_page_id = 'your_facebook_page_id'

# 設置 Twitter API 客戶端
auth = tweepy.OAuth1UserHandler(consumer_key=twitter_consumer_key,
                                consumer_secret=twitter_consumer_secret,
                                access_token=twitter_access_token,
                                access_token_secret=twitter_access_token_secret)
twitter_api = tweepy.API(auth)

# 設置 Facebook API 客戶端
facebook_api = facebook.GraphAPI(access_token=facebook_access_token)

def post_twitter(message):
    try:
        twitter_api.update_status(message)
        logging.info(f"{datetime.now()} - Twitter: 發送成功")
    except Exception as e:
        logging.error(f"{datetime.now()} - Twitter 發送失敗: {str(e)}")

def post_facebook(message):
    try:
        facebook_api.put_object(parent_object=facebook_page_id, connection_name='feed', message=message)
        logging.info(f"{datetime.now()} - Facebook: 發送成功")
    except Exception as e:
        logging.error(f"{datetime.now()} - Facebook 發送失敗: {str(e)}")

# 定時發文
def schedule_posts():
    schedule.every().day.at("09:00").do(post_twitter, message="Good morning from Twitter!")
    schedule.every().day.at("09:00").do(post_facebook, message="Good morning from Facebook!")

    schedule.every().monday.at("10:00").do(post_twitter, message="Weekly update from Twitter!")
    schedule.every().monday.at("10:00").do(post_facebook, message="Weekly update from Facebook!")

# 執行定時任務
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60) 

if __name__ == "__main__":
    schedule_posts()
    run_scheduler()
