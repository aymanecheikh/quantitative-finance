from pprint import pprint
import xml.etree.ElementTree as ET
import re
filename: str = 'req_scanner_parameters.xml'


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


## Start trying out the extracted filters?


if __name__ == '__main__':
    asset_classes = get_asset_classes()
    for i in asset_classes:
        try:
            pprint(i['filters'])
        except KeyError as e:
            continue
