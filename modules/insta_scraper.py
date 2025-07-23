from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time, os
from dotenv import load_dotenv

def scrape_instagram_comments(url):
    print("[Instagram] Starting scraper...")
    load_dotenv()
    username = os.getenv("INSTA_USERNAME")
    password = os.getenv("INSTA_PASSWORD")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    if username is None:
        raise ValueError("INSTA_USERNAME environment variable not set.")
    driver.find_element(By.NAME, "username").send_keys(username)
    if password is None:
        raise ValueError("INSTA_PASSWORD environment variable not set.")
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(6)

    driver.get(url)
    time.sleep(5)

    # Load more comments if available
    try:
        for _ in range(10):
            driver.find_element(By.XPATH, '//button[contains(text(), "View all comments")]').click()
            time.sleep(2)
    except:
        pass

    try:
        for _ in range(10):
            driver.find_element(By.XPATH, '//button[contains(text(), "Load more comments")]').click()
            time.sleep(2)
    except:
        pass

    comments = driver.find_elements(By.CSS_SELECTOR, "ul._a9ym > li > div > div > div > span")
    comment_list = [c.text for c in comments if c.text.strip()]

    os.makedirs("output", exist_ok=True)
    pd.DataFrame(comment_list, columns=["Instagram Comments"]).to_excel("output/instagram_comments.xlsx", index=False)

    print(f"[Instagram] Scraped {len(comment_list)} comments.")
    driver.quit()
