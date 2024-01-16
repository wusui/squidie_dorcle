# Copyright (C) 2024 Warren Usui, MIT License
"""
Selenium driver interface
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """
    Use Service to get the driver
    """
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def start_selenium(suffix):
    """
    Selenium start routine.
        suffix -- path added to webpage to select quiz type
        returns driver
    """
    def ex_w_driver(driver):
        driver.get(f"https://www.sedecordle.com/{suffix}")
        return driver
    return ex_w_driver(get_driver())

def handle_word_input(guess_pckt):
    """
    Inputs a word
    Guess_pckt is a dictionary with the following key/values:
        'driver': Selenium driver
        'guess': word input by user
    """
    list(map(lambda a: guess_pckt['driver'].find_element(By.ID, a).click(),
             guess_pckt['guess']))
    guess_pckt['driver'].find_element(By.ID, 'enter2').click()

def read_word_set(wset_pckt):
    """
    Read one of the 16 sedecordle sets
    Wset_pckt values:
        'driver': Selenium driver
        'set': number of set read
    """
    def find_nblank(word_num):
        return wset_pckt['driver'].find_element(By.ID,
                f"box{wset_pckt['set']},{word_num},1").text
    def rws_int_word(windx):
        def riw_letter(lnumb):
            def get_chr_info(elem_obj):
                return [elem_obj.text,
                        elem_obj.value_of_css_property('background-color')]
            return get_chr_info(wset_pckt['driver'].find_element(By.ID,
                    f"box{wset_pckt['set']},{windx},{lnumb}"))
        return list(map(riw_letter, list(range(1,6))))
    def word_format(one_word):
        def fix_bg_col(one_letter):
            return [one_letter[0], {'24': 'B', '0': 'G', '255': 'Y'}
                    [one_letter[1].split('(')[-1].split(',')[0]]]
        return list(map(list, zip(*list(map(fix_bg_col, one_word)))))
    def rws_refmt(raw_data):
        return list(map(word_format, raw_data))
    def rws_gsize(guess_cnt):
        return list(map(rws_int_word, guess_cnt))
    return rws_refmt(rws_gsize(list(filter(find_nblank, list(range(1,22))))))
