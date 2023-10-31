import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options


def scraping(driver, url):
    data_dict = dict()
    driver.get(url)
    time.sleep(5)
    container = driver.find_element(By.CLASS_NAME, "scroll__container")
    # while True:
    #     position = driver.execute_script("return arguments[0].scrollTop;", container)
    #     time.sleep(1)
    #     driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
    #     if position == driver.execute_script("return arguments[0].scrollTop;", container):
    #         break
    for _ in range(3):
        time.sleep(1)
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
    for url_scrap in driver.find_elements(By.CLASS_NAME, "search-snippet-view"):
        time.sleep(1)
        category = url_scrap.find_element(By.CLASS_NAME, "search-business-snippet-view__category").text
        lat = ''
        lan = ''
        address = ""
        url_open = url_scrap.find_element(By.CLASS_NAME, "search-business-snippet-view__address").get_attribute("href")
        if url_open is not None:
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url_open)
            time.sleep(2)
            lat = driver.find_element(By.CLASS_NAME, "toponym-card-title-view__coords-badge").text.split(",")[0]
            lan = driver.find_element(By.CLASS_NAME, "toponym-card-title-view__coords-badge").text.split(",")[1]
            address = driver.find_element(By.CLASS_NAME, "toponym-card-title-view__description").text
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        print(category, lat, lan, address)
        data_dict[url_scrap] = [category, lat, lan, address]
    time.sleep(5)
    return data_dict


def main():
    url = ("https://yandex.ru/maps/?filter=chain_id%3A2129228517&ll=70.388531%2C28."
           "620518&mode=search&sll=70.388531%2C28.62"
           "0518&sspn=265.429687%2C151.366169&text=Wildberries&z=2")
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(r"C:\Users\pirve\PycharmProjects\test\chromedriver", options=chrome_options)
    returned_data = scraping(driver=driver, url=url)

    data = list()
    for key, val in returned_data.items():
        print(key, val)
        data.append({
            'Category': val[0],
            'Lat': val[1],
            'Lan': val[2],
            'Address': val[3]
        })

    df = pd.DataFrame(data)
    df.to_excel(r'test_file.xlsx', index=False)


if __name__ == "__main__":
    main()
