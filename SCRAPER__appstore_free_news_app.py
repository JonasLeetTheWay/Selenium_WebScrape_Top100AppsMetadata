from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas as pd

def click_and_wait(e,wait_second=10):
    e.click()
    driver.implicitly_wait(wait_second)


def get_image_url(srcset, size):
    '''
sizes = 640, 320, 314, 292, 157, 146

:Returns (str):
\n url with the closest width to the desired pixel size.
    '''
    urls = srcset.split(", ")
    for url in urls:
        print('url: ',url)
        url_size = int(url.split("/")[-1].split("x")[0])
        if url_size >= size:
            return url.split(" ")[0]
    return urls[-1].split(" ")[0]


chromedriver_path = "C:\\Packages_N_Drivers\\chromedriver.exe"
driver_service = Service(chromedriver_path)
driver = webdriver.Chrome(service=driver_service)

# url = 'https://apps.apple.com/tw/charts/iphone/%E6%96%B0%E8%81%9E-apps/6009'
url = 'https://apps.apple.com/tw/charts/iphone/%E6%96%B0%E8%81%9E-apps/6009?chart=top-free' # free apps

driver.get(url)

# Create an empty list to store the app data
app_data = []

app_category = driver.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/section[1]/div[1]/div/h1')
apps = driver.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/section[2]/ol').find_elements(By.TAG_NAME,'li')

print('app category: ',app_category.text)
print('apps count: ', len(apps))

for idx, app in enumerate(apps):
    app_link = app.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a')
    app_icon = app_link.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a/div[1]')
    app_icon_picture = app_icon.find_element(By.XPATH,f'//*[@id="ember{idx+28}"]/source[2]')
    app_metadata = app_link.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a/div[2]')
    app_rank = app_metadata.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a/div[2]/p')
    app_title = app_metadata.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a/div[2]/div/div[1]')
    app_company = app_metadata.find_element(By.XPATH,f'//*[@id="charts-content-section"]/ol/li[{idx+1}]/a/div[2]/div/div[2]')

      # Create a dictionary to store the app data
    app_dict = {
        'category': app_category.text,
        'rank': app_rank.text,
        'title': app_title.text,
        'company': app_company.text,
        'icon_url': get_image_url(app_icon_picture.get_attribute('srcset'), 320), #choose sizes = 640, 320, 314, 292, 157, 146
        'link': app_link.get_attribute('href')
    }

     # Append the dictionary to the list of app data
    app_data.append(app_dict)

# Create a Pandas DataFrame from the app data
df = pd.DataFrame(app_data)

# Display the DataFrame
print(df.head())
df.to_excel('appstore_free_news_app_top100_data.xlsx', index=False)



# app_sections_block_xpath = '//*[@id="charts-content-section"]'

# app_category = driver.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/section[1]/div[1]/div/h1')
# print(app_category.text)
# app_sections_block = driver.find_element(By.XPATH,'//*[@id="charts-content-section"]/div[1]/div/section')
# print(app_sections_block.text)
# app_sections = driver.find_element(By.XPATH,'//*[@id="charts-content-section"]').find_elements(By.TAG_NAME,'div')    #.find_elements(By.CLASS_NAME,'l-row chart')
# for app_section in app_sections:
#     section = app_section.find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'section')
#     section_nav = section.find_element(By.TAG_NAME,'div')
#     # print the app-price-type whether its free or not free
#     print(section_nav.find_element(By.TAG_NAME,'h2').text)
#     # find tag to show all apps
#     all_apps_in_section = section_nav.find_element(By.TAG_NAME,'a')
#     click_and_wait(all_apps_in_section,15)

#######################

# e1_xpath = '/html/body/div[3]/main/div[2]/section[1]/div[2]/div/div/div[2]/div/button[1]'
# e2_xpath = '/html/body/div[3]/main/div[2]/section[1]/div[2]/div/div/div[2]/div/div/div[1]'
# e1 = driver.find_element(By.XPATH,e1_xpath)
# click_and_wait(e1)

# e2 = e1.find_element(By.XPATH,e2_xpath)
# e1_elements = e2.find_elements(By.TAG_NAME,'a')

# for ele in e1_elements:
#     print(ele.text)'

'''
/html/body/div[3]/main/div[2]/section[1]/div[1]/div -> output Category text

section section--bordered -> general div to hold list of apps 
section__nav -> enter another div to detertime whether the apps shown are  free or not-free

// from this level downwards, we can get aTag or headlineText

section__headline section__headline--app -> get headlineText
driver.find_elements(By.TAG_NAME,'a') -> get aTag

'''



# for ele in e1_elements:
#     click_and_wait(ele)

#     CATEGORY_TEXT = ele.find_element(By.XPATH,'/html/body/div[3]/main/div[2]/section[1]/div[1]/div').text
#     print('CATEGORY_TEXT: ',CATEGORY_TEXT)

#     app_sections = ele.find_elements(By.CLASS_NAME,'section section--bordered')
#     for app_section in app_sections:
#         app_section.find_element(By.CLASS_NAME,'section__nav')
#         # print the app-price-type whether its free or not free
#         print(app_section.find_element(By.CLASS_NAME,'section__headline section__headline--app').text)
#         # find tag to show all apps
#         all_apps_in_section = app_section.find_element(By.TAG_NAME,'a')
#         click_and_wait(all_apps_in_section,15)




# url = 'https://the-internet.herokuapp.com/dynamic_loading/2'
# driver.get(url)
# driver.find_element("xpath", '//*[@id="start"]/button').click()
# driver.implicitly_wait(10)
# text = driver.find_element("xpath", '//*[@id="finish"]/h4').text
