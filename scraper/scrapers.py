from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from .models import MyDashOne, ScrapedData
from bs4 import BeautifulSoup
from .models import ScrapedData
import time

def save_to_db(all_data):
    for data in all_data:
        existing = ScrapedData.objects.filter(username=data["USERNAME"]).exists()
        # date_object = datetime.datetime.strptime(data["LAST_LOGIN"], "%Y-%m-%d %H:%M:%S").date()
        if existing:
            m = ScrapedData.objects.get(username=data["USERNAME"])
            m.last_login = data["LAST_LOGIN"]
            m.save()
        else:
            m = ScrapedData(username=data["USERNAME"], channel=data["CHANNEL"], last_login=data["LAST_LOGIN"], user_agent=data["USER_AGENT"])
            m.save()
    print("done saving to the database!")

def handleScraping(driver, mydash):
    print("getting started with data scraping...")
    page_source = BeautifulSoup(driver.page_source, 'lxml')
    all_tr = page_source.find_all("tr")
    extract = []
    for i,tr in enumerate(all_tr):
        if i == 0:
            continue
        all_td = tr.find_all("td")
        to_what = {}
        for ind,td in enumerate(all_td):
            val = td.string
            if ind == 0:
                to_what["USERNAME"] = val
            elif ind == 1:
                to_what["CHANNEL"] = val
            elif ind == 4:
                to_what["USER_AGENT"] = val
        else:
            currentdatetime = datetime.now()
            to_what["LAST_LOGIN"] = str(currentdatetime)
            extract.append(to_what)
    # both all_tr and extract are empty------- login password not working
    # all_tr is not empty but extract is empty--- no user is online
    driver.quit()

    if all_tr and extract:
        # save here
        print(extract)

        save_to_db(extract)

        mydash.engineIsSafe = True
        mydash.save()
    elif not all_tr and not extract:
        mydash.engineIsSafe = False
        mydash.save()
        print("password incorrect or mydash.one has changed their web design.")
    elif all_tr and not extract:
        print("no user is currently online!")

    # cleanup
    extract = []

def scrape(login_url, activityLogUrl):
    mydash = MyDashOne.objects.all()[0]
    payload = {
    "username": mydash.username,
    "password": mydash.password,
    }

    # login to mydash.one
    options = ChromeOptions()
    options.add_argument(" - incognito")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    print("Establishing connection...")
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(login_url)

    driver.find_element(By.NAME, "username").send_keys(payload["username"])
    driver.find_element(By.NAME, "password").send_keys(payload["password"])
    driver.find_element(By.CSS_SELECTOR, "[type=submit]:not(:disabled)").click()
    
    # scraping from mydash.one
    time.sleep(0.3) 
    driver.get(activityLogUrl)
    time.sleep(10)
    handleScraping(driver, mydash)