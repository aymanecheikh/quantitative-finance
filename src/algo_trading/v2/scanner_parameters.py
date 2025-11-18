import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from api_client import run_server
filename: str = 'log/scanner.xml'

def gtext(node, names):
    for n in names:
        el = node.find(n)
        if el is not None and el.text and el.text.strip():
            return el.text.strip()
    return ""

def dump_scanner_params(host='127.0.0.1', port=4002, client_id=0, outdir=Path('.')):
    app = run_server()

    xml = app.reqScannerParameters()
    app.disconnect()
    tree = ET.parse(filename)
    root = tree.getroot()
    # root = ET.fromstring('log/scanner.xml')

    scan_types = []
    for st in root.findall('.//ScanType') + root.findall('.//scan_type'):
        scan_types.append({
            'code': gtext(st, ['displayName', 'display_name']),
        })
    seen = set()
    uniq_scan_types = []
    for d in scan_types:
        key = (d['code'], d['display_name'])
        if d['code'] and key not in seen:
            uniq_scan_types.append(d)
            seen.add(key)
    uniq_scan_types.sort(key=lambda x: (x['display_name'].lower(), x['code']))

    outdir.mkdir(parents=True, exist_ok=True)

    (outdir / 'scanner_scan_types.json').write_text(json.dumps(uniq_scan_types, indent=2))
    (outdir / 'scanner_filter_fields.json').write_text(json.dumps(uniq_filters, indentt=2))

    with open(outdir / 'scanner_scan_types.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['code', 'display_name'])
        w.writeheader(); w.writerows(uniq_scan_types)

    print(f'Scan types: {len(uniq_scan_types)}')
    print(f'Filter fields: {len(uniq_filters)}')
    print(f'Wrote files to {outdir.resolve()}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Dump IBKR scanner params to CSV/JSON')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=4002)
    ap.add_argument('--client-id', type=int, default=0)
    ap.add_argument('--outdir', default='ibkr_scanner_params')
    args = ap.parse_args()
    dump_scanner_params(args.host, args.port, args.client_id, Path(args.outdir))
