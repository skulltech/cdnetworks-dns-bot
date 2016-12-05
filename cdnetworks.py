from configparser import ConfigParser
import time
import sys

import wdstart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as SE


class CDNetworksBot:
    def __init__(self):
        config = ConfigParser()
        config.read_file(open('config.ini', mode='r', encoding='utf8'))
        if not config.has_section('CREDENTIALS')::
            print('Config file not available or correctly configured! Exiting.')
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

    def add_zone(self, domain_name, zone_ttl, soa_email, soa_ttl, serial_num):
        self.driver.get('https://control.cdnetworks.com/dns/zone/new/?m=268')

        self.driver.find_element_by_name('zone_name').send_keys(domain_name)
        self.driver.find_element_by_name('zone_ttl').clear()
        self.driver.find_element_by_name('zone_ttl').send_keys(zone_ttl)
        self.driver.find_element_by_name('soa_email').clear()
        self.driver.find_element_by_name('soa_email').send_keys(soa_email)
        self.driver.find_element_by_name('soa_ttl').send_keys(soa_ttl)
        self.driver.find_element_by_id('id_soa_serial_num_choices_1').click()
        self.driver.find_element_by_name('soa_serial_num').send_keys(serial_num)

        self.driver.find_element_by_id('btn_add_domain').click()
        self.driver.find_element_by_id('confirm_zone_yes').click()

    def delete_zone(self, domain_name):
        self.driver.get('https://control.cdnetworks.com/dns/zones_list/?m=268')

        self.driver.find_element_by_id('txt_search').send_keys(domain_name)
        self.driver.find_element_by_id('btn_search').click()

        self.driver.find_element_by_xpath('//a[@class="btn-delete" and @data-name="{}"]'.format(domain_name)).click()
        self.driver.find_element_by_xpath('//div[@id="notify"]//button[@id="btn_delete_yes"]').click()
