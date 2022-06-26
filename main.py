
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import telebot
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')
"/app/.chromedriver/bin/chromedriver"
bot = telebot.TeleBot(API_KEY)
chrome_options = Options()
chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
op.add_argument("--headless")
op.add_argument('--no-sandbox')
op.add_argument("--disable-dev-sh-usage")

def access_Web():
    #driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
    driver=webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),chrome_options=op)
    driver.get('https://hdtoday.tv/home')

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    app = soup.find('div', attrs={'id': 'app'})
    wrapper = app.find('div', attrs={'id': 'wrapper'})
    main_wrapper = wrapper.find('div', attrs={'id': 'main-wrapper'})
    container = main_wrapper.find('div', attrs={'class': 'container'})
    section = container.find('section', attrs={'class': 'block_area block_area_home section-id-01'})
    tab = section.find('div', attrs={'class': 'tab-content'})
    return tab


@bot.message_handler(commands=['Movies'])
def Movies(message):
    tab = access_Web()
    trending_M = tab.find('div', attrs={'id': 'trending-movies'})
    block = trending_M.find('div', attrs={'class': 'block_area-content block_area-list film_list film_list-grid'})
    f_wrap = block.find('div', attrs={'class': 'film_list-wrap'})
    i = 0
    for a in f_wrap.find_all('div', attrs={'class': 'flw-item'}):

        poster = a.find('div', attrs={'class': 'film-poster'})
        quality = poster.find('div', attrs={'class': 'pick film-poster-quality'})
        the_one = poster.find('a')
        images = poster.find('img')
        print(images['data-src'])
        img = requests.get(images['data-src'])
        #importtant
        print(the_one['title'] + ' ' + quality.text)
        bot.send_message(message.chat.id, the_one['title'] + ' ' + quality.text)
        bot.send_photo(message.chat.id, img.content)
        i = i + 1
        if i > 10:
            break
   #pushing

@bot.message_handler(commands=['Series'])
def Series(message):
    tab = access_Web()

    trending_S = tab.find('div', attrs={'id': 'trending-tv'})
    block = trending_S.find('div', attrs={'class': 'block_area-content block_area-list film_list film_list-grid'})
    f_wrap = block.find('div', attrs={'class': 'film_list-wrap'})

    i = 0
    for a in f_wrap.find_all('div', attrs={'class': 'flw-item'}):

        poster = a.find('div', attrs={'class': 'film-poster'})
        quality = poster.find('div', attrs={'class': 'pick film-poster-quality'})
        the_one = poster.find('a')
        images = poster.find('img')
        print(images['data-src'])
        img = requests.get(images['data-src'])

        print(the_one['title'] + ' ' + quality.text)
        # telegram_send.send(messages=[the_one['title'] + ' ' + quality.text], images=[img.content])
        bot.send_message(message.chat.id, the_one['title'] + ' ' + quality.text)
        bot.send_photo(message.chat.id, img.content)
        i = i + 1
        if i > 10:
            break


bot.polling()
