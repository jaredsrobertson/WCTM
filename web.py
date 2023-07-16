import undetected_chromedriver as uc
#import os
from dotenv import dotenv_values
from retry import retry
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

#chrome_profile = os.getenv('chrome_profile')
config = dotenv_values('.env')

options = uc.options.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
options.add_argument('--user-data-dir=' + config['chrome_profile'])
options.add_argument('--profile-directory=python')
options.add_argument('--hide-crash-restore-bubble')
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

@retry((Exception), tries=3, delay=5, backoff=0)
async def get_rank(steam_id):
    driver.get(f"https://rocketleague.tracker.network/rocket-league/profile/steam/{steam_id}/overview")
    rank_find = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[contains(text(),' Ranked Standard 3v3 ')]")))
    rank_data = rank_find.find_element(By.XPATH, ".//following-sibling::div[contains(@class, 'rank')]").text
    rank = rank_data.split("•")[0]
    num = len(rank.split()[1])
    rankimg = rank[:1].lower() + str(num)
    return rank, rankimg

def exit():
    driver.close()
    driver.quit()
    return