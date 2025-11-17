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

def get_scanner_layouts() -> list:
    instrument_list = [child for child in root[6]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_instrument_groups() -> list:
    instrument_list = [child for child in root[7]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_similar_products_defaults() -> list:
    instrument_list = [child for child in root[8]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def main_screen_default_tickers() -> list:
    instrument_list = [child for child in root[9]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_column_sets() -> list:
    instrument_list = [child for child in root[10]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details


def get_sidecar_scanner_defaults() -> list:
    instrument_list = [child for child in root[11]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_advanced_scanner_defaults() -> list:
    instrument_list = [child for child in root[12]]
    instrument_list_details = []
    for i in range(len(instrument_list)):
        detail_entry = {}
        for j in range(len(instrument_list[i])):
            item = instrument_list[i][j]
            detail_entry[item.tag] = item.text
        instrument_list_details.append(detail_entry)

    return instrument_list_details

def get_filter_list() -> list:
    instrument_list = [child for child in root[13]]
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
    # scanner_layouts = get_scanner_layouts()
    instrument_groups = get_instrument_groups()
    # similar_products_defaults = get_similar_products_defaults()
    # main_screen_default_tickers = main_screen_default_tickers()
    column_sets = get_column_sets()
    # sidecar_scanner_defaults = get_sidecar_scanner_defaults()
    # advanced_scanner_defaults = get_advanced_scanner_defaults()
    filter_list = get_filter_list()


