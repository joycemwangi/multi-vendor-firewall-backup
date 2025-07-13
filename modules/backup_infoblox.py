"""
backup_infoblox.py

Module to perform automated backups of Infoblox DNS/DHCP configurations
using Infoblox REST API (WAPI).

Prerequisites:
- Infoblox IP and credentials configured in devices.yaml
- Python requests module installed
- API user must have permission to access configuration objects

Usage:
- Called internally by backup_firewalls.py
- Customize API version or endpoints here if needed

Note:
- Handle SSL verification based on your Infoblox setup (verify=False can be used for self-signed certs)
- Replace placeholders with actual IP, username, and password in devices.yaml
"""

import requests
import os
import datetime
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def backup_infoblox(device):
    try:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_path = 'backups/infoblox'
        os.makedirs(base_path, exist_ok=True)

        url = f"https://{device['ip']}/wapi/v2.10/record:host"
        response = requests.get(url,
                                auth=HTTPBasicAuth(device['username'], device['password']),
                                verify=False)

        if response.status_code != 200:
            raise Exception(f"Infoblox API error: {response.status_code} {response.text}")

        file_path = f"{base_path}/{device['name']}_{now}.json"
        with open(file_path, 'w') as f:
            f.write(response.text)

        print(f"[✓] Infoblox backup saved to {file_path}")

    except Exception as e:
        print(f"[!] Infoblox backup failed: {e}")
