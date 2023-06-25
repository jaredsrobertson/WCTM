from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

chrome_options = uc.options.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless=new')
#driver = webdriver.Chrome(options=chrome_options)
driver = uc.Chrome(options=chrome_options)
ua = UserAgent()
chrome_options.add_argument(f'user-agent={ua.random}')

wait = WebDriverWait(driver, 10)


def scrape_rank(pname):
    driver.get(f"https://rocketleague.tracker.network/rocket-league/profile/steam/{pname}/overview")
    ranks_table = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "div.trn-table__container>table>tbody")))
    rank_3v3 = ranks_table.find_element(By.XPATH, "//tr//td[@class='name']//div[contains(text(),'Standard "
                                                  "3v3')]/following-sibling::div")

    rank_text = rank_3v3.text
    rank = rank_text.split('\n')[0]
    #driver.close()
    return rank

