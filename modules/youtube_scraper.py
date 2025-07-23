import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scrape_youtube_comments(url):
    print("[YouTube] Starting scraper...")

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # Launch Chrome browser
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)

        # Scroll to load comments section
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(3)

        for _ in range(20):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)

        # Extract visible comments
        comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
        comment_list = [c.text.strip() for c in comments if c.text.strip()]

        # Create output directory inside main project folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "youtube_comments.xlsx")

        # Save to Excel
        pd.DataFrame(comment_list, columns=["YouTube Comments"]).to_excel(output_path, index=False)

        print(f"[YouTube] Scraped {len(comment_list)} comments.")
        print(f"[YouTube] Comments saved to: {output_path}")

    except Exception as e:
        print(f"[YouTube] Error: {e}")
        raise

    finally:
        driver.quit()
