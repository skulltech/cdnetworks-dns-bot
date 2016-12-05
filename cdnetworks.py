import time
import sys
import csv
import os
from configparser import ConfigParser

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
        if not config.has_section('CREDENTIALS'):
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
        if zone_ttl:
            self.driver.find_element_by_name('zone_ttl').clear()
            self.driver.find_element_by_name('zone_ttl').send_keys(zone_ttl)
        if soa_email:
            self.driver.find_element_by_name('soa_email').clear()
            self.driver.find_element_by_name('soa_email').send_keys(soa_email)
        if soa_ttl:
            self.driver.find_element_by_name('soa_ttl').send_keys(soa_ttl)
        if serial_num:
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


def add_zones(csvfile, cdnetworksbot):
    for row in csvfile:
        cdnetworksbot.add_zone(domain_name=row[0], zone_ttl=row[1], soa_email=row[2], soa_ttl=row[3], serial_num=row[4])

def delete_zones(csvfile, cdnetworksbot):
    for row in csvfile:
        cdnetworksbot.delete_zone(domain_name=row[0])

def main():
    input_file = input('Enter the filename of input CSV (leave blank for "input.csv"): ')
    if not input_file:
        input_file = 'input.csv'
    if not os.path.exists(input_file):
        print('CSV file not found! Exiting.')
        sys.exit()

    try:
        argument = sys.argv[1]
    except IndexError:
        print('No command-line argument provided! Exiting')
        sys.exit()

    with open(input_file, mode='r') as f:
        csvfile = csv.reader(f)

        if argument == 'add':
            cdnetworksbot = CDNetworksBot()
            cdnetworksbot.login()
            add_zones(csvfile, cdnetworksbot)
        elif argument == 'delete':
            cdnetworksbot = CDNetworksBot()
            cdnetworksbot.login()
            delete_zones(csvfile, cdnetworksbot)
        else:
            print('Invalid command-line arguments! Exiting')
            sys.exit()


if __name__=='__main__':
    main()