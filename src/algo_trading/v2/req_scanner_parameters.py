from pprint import pprint
import xml.etree.ElementTree as ET
import time
import threading
import re
from api_client import IBapi
filename: str = 'log/scanner.xml'


## Note to self:
## There appears to be consistency in fetching immediate root
## children
## We can group into one master object or maybe json
## For now I will take the "dumb" approach and continue exploring

def get_scanner_params():
    app = run_server()
    app.reqScannerParameters()


tree = ET.parse(filename)
root = tree.getroot()
tags = [child.tag for child in root]


def get_asset_classes() -> list:
    instrument_list = [child for child in root[0]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            if item.tag == 'filters':
                item.text = item.text.split(',')
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_locations() -> list:
    instrument_list = [child for child in root[2]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_scan_codes() -> list:
    instrument_list = [child for child in root[3]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_settings_list() -> list:
    instrument_list = [child for child in root[4]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_filter_list() -> list:
    instrument_list = [child for child in root[5]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details



if __name__ == '__main__':
    asset_classes = get_asset_classes()
    locations = get_locations()
    scan_codes = get_scan_codes()
    settings = get_settings_list()
    filters = get_filter_list()
