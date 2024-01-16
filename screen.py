# Copyright (C) 2024 Warren Usui, MIT License
"""
Screen actions
"""
import time
from selenium.webdriver.common.by import By

def scroll_move(packet):
    """
    Scroll image.  Packet contains:
        driver: Selenium driver
        word_numb: Word number to scroll to
    """
    def do_steps(step_number):
        def find_first_blank():
            if step_number != packet['word_numb']:
                return 22
            return len(list(filter(lambda a:
                    len(packet['driver'].find_element(By.ID,
                    f"box{step_number},{a},1").text) != 0,
                    list(range(1, 22))))) + 1
        def skipper(row_number):
            if step_number == packet['word_numb']:
                if len(packet['driver'].find_element(By.ID,
                        f"box{step_number},{row_number},1").text) == 0:
                    packet['driver'].execute_script(
                                "arguments[0].scrollIntoView();",
                                packet['driver'].find_element(By.ID,
                                f"box{step_number},{row_number},1"))
                    return
                time.sleep(.2)
            time.sleep(.05)
            packet['driver'].execute_script(
                                "arguments[0].scrollIntoView();",
                                packet['driver'].find_element(By.ID,
                                f"box{step_number},{row_number},1"))
        list(map(skipper, list(range(1, find_first_blank()))))
    def do_action(start):
        list(map(do_steps, range(start, packet['word_numb'] + 2, 2)))
    packet['driver'].execute_script("arguments[0].scrollIntoView();",
                                    packet['driver'].find_element(By.ID,
                                    "box1,1,1"))
    do_action(2 - packet['word_numb'] % 2)
