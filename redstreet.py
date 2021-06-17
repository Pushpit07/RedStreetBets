from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta
from dateutil.parser import parse
import requests

url = 'https://www.reddit.com/r/wallstreetbets/search/?q=flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new'

options = Options()
options.headless = True

browser = webdriver.Chrome(options=options)
browser.get(url)

yesterday = date.today() - timedelta(days=1)
links = browser.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')

#######################################
#  START: Get the link for yesterday  #
#######################################

for a in links:
    if a.text.startswith('Daily Discussion Thread'):
        date = "".join(a.text.split(' ')[-3:])
        parsed = parse(date)
        if parse(str(yesterday)) == parsed:
            link = a.find_element_by_xpath('../..').get_attribute('href')

    if a.text.startswith('Weekend'):
        weekend_date = a.text.split(' ')
        parsed_date = weekend_date[-3] + ' ' + weekend_date[-2].split("-")[1] + weekend_date[-1]
        parsed = parse(parsed_date)
        saturday = weekend_date[-3] + ' ' + str(int(weekend_date[-2].split(
            "-")[1].replace(',', '')) - 1) + ' ' + weekend_date[-1]

        if parse(str(yesterday)) == parsed:
            link = a.find_element_by_xpath('../..').get_attribute('href')

        elif parse(str(yesterday)) == parse(str(saturday)):
            link = a.find_element_by_xpath('../..').get_attribute('href')

stock_link = link.split('/')[-3]
print(stock_link)

html = requests.get(f'https://api.pushshift.io/reddit/submission/comment_ids/{stock_link}')

raw_comment_list = html.json()
browser.close()

print(raw_comment_list)