import undetected_chromedriver as driver_
import time
from selenium.webdriver.common.by import By
from src.Backend.SourceMonitoring.app.api.Parsing_information_data_storage import Information


def Driver(url):
    driver = driver_.Chrome(use_subprocess=False)
    driver.get(url)
    driver.maximize_window()
    ScrollPage(driver)

def ScrollPage(driver):
    while True:
        height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.0)
        FindElements(driver)
        if height == 0:
            print("Прокрутка завершена")
            driver.quit()
            break


def FindElements(driver):
    Names = driver.find_elements(By.CLASS_NAME, "_2ic-qMvB--Ui")
    Informations = driver.find_elements(By.CLASS_NAME, "_1Gi_2LTOIonK")
    Dates = driver.find_elements(By.CLASS_NAME, "_3lgXtV6o5Jma")
    Urls = driver.find_elements(By.CLASS_NAME, "_2ic-qMvB--Ui")
    UrlPhotos = driver.find_elements(By.CLASS_NAME, "_2DhpGRcOry9t")
    AddInformations(Names, Informations, Dates, Urls, UrlPhotos)

def AddInformations(Names, Informations, Dates, Urls, UrlPhotos):
    ListInf = []

    for i in range(len(Names)):
        Inf = Information(Names[i].text, Informations[i].find_element(By.TAG_NAME, "p").text, Dates[i].text, Urls[i].get_attribute('href'),
                          UrlPhotos[i].find_elements(By.CLASS_NAME, "_17cXL8rzC79K")[1].value_of_css_property("background-image")[5:-2])
        ListInf.append(Inf)

    for i in ListInf:
        print(f"{i.name} \n{i.info} \n{i.data} \n{i.url} \n{i.url_photo}\n")

def ParseSite():
    url = "https://leader-id.ru/navigator?sort=new"
    Driver(url)

if __name__ == '__main__':
    ParseSite()