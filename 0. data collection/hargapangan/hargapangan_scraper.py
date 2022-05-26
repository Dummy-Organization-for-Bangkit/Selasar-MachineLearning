from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# To prevent download dialog
#profile = webdriver.FirefoxProfile()
#profile.set_preference('browser.download.folderList', 2) # custom location
#profile.set_preference('browser.download.manager.showWhenStarting', False)
#profile.set_preference('browser.download.dir', '/tmp')
#profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

#browser = webdriver.Firefox(profile)
#browser.get("http://hargapangan.id/tabel-harga/pasar-tradisional/daerah")

#options = webdriver.ChromeOptions()
#prefs = {'download.default_directory':'C:\\Users\\WINDOWS 10\\Downloads'}
#example: prefs = {"download.default_directory" : "C:\Tutorial\down"};
#options.add_experimental_option("prefs",prefs);

#driver = webdriver.Chrome(executable_path="C:\\Users\\WINDOWS 10\\misc\\chromedriver.exe", options=options)
    
jakarta = {
    'province': 'DKI Jakarta', 
    'city': 'Kota Jakarta Pusat'
    }
bogor = {
    'province': 'Jawa Barat',
    'city': 'Kota Bogor'
    }

depok = {
    'province': 'Jawa Barat',
    'city': 'Kota Depok'
    }

tangerang = {
    'province': 'Banten',
    'city': 'Kota Tangerang'
    }

bekasi = {
    'province': 'Jawa Barat',
    'city': 'Kota Bekasi'
    }

def download_price_data(location, today_date=True):
    province = location['province']
    city = location['city']
    DESTINATION = 'C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\raw\\{}'.format(city)

    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory':DESTINATION}
    options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(executable_path="C:\\Users\\WINDOWS 10\\misc\\chromedriver.exe", options=options)

    driver.get('http://hargapangan.id/tabel-harga/pasar-tradisional/daerah')
    driver.implicitly_wait(10)

    get_province = driver.find_element(By.XPATH, '//option[text()="{}"]'.format(province))

    try:
        get_province.click()

        get_city = driver.find_element(By.XPATH, '//option[text()="{}"]'.format(city))
        get_city.click()

        click_download = driver.find_element(By.ID, 'btnDownload')

        click_download.click()

        time.sleep(5)

        driver.close()
    except:
        print('Invalid')

download_price_data(jakarta)
download_price_data(bogor)
download_price_data(depok)
download_price_data(tangerang)
download_price_data(bekasi)