# Copyright (C) 2024 Warren Usui, MIT License
"""
Crudely scrape the dictionary from the sedecordle web page
"""
import requests

def read_data():
    """
    Read the sedecordle web page
    """
    return requests.get('https://www.sedecordle.com', timeout=30).text

def get_dict():
    """
    Extract the sedecordle dictionary from the web page
    """
    def gd_inner(itext):
        return itext[itext.find('answers = '):].split('"')[1].split(' ')
    return gd_inner(read_data())
