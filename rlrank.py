import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

chrome_options = uc.options.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless=new')
chrome_options.add_argument(f'user-agent={UserAgent().random}')
driver = uc.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)


def scrape_rank(pname):
    driver.get(f"https://rocketleague.tracker.network/rocket-league/profile/steam/{pname}/overview")
    ranks_table = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "div.trn-table__container>table>tbody")))
    rank_3v3 = ranks_table.find_element(By.XPATH, "//tr//td[@class='name']//div[contains(text(),'Standard 3v3')]/following-sibling::div")

    rank = rank_3v3.text #full rank
    num = len(rank.split()[1])
    rankimg = rank[:1].lower() + str(num)
    return rank, rankimg
    #driver.close()