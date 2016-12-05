from configparser import ConfigParser

import wdstart
import selenium.common.exceptions as SE
from selenium import webdriver


class CDNetworksBot:
    def __init__(self):
        config = ConfigParser()
        config.read_file(open('config.ini', mode='r', encoding='utf8'))
        if not config:
            print('Config file not available!')
            sys.exit()

        self.USERNAME = config['CREDENTIALS']['Username']
        self.PASSWORD = config['CREDENTIALS']['Password']
        self.driver = wdstart.start_webdriver(driver_name='chrome')

    def login(self):
        self.driver.get('https://control.cdnetworks.com/')
        username_elem = self.driver.find_element_by_name('username')
        password_elem = self.driver.find_element_by_name('password')

        username_elem.send_keys(self.USERNAME)
        password_elem.send_keys(self.PASSWORD)
        self.driver.find_element_by_name('login').click()

bot = CDNetworksBot()
bot.login()