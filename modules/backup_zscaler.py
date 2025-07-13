"""
backup_zscaler.py

Module to backup Zscaler configurations using Zscaler API.

NOTE:
- Replace API key and credentials in this module or via environment variables.
- See README for instructions on generating API keys.
"""

import requests
import os
import datetime

def backup_zscaler(device):
    try:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_path = 'backups/zscaler'
        os.makedirs(base_path, exist_ok=True)

        session = requests.Session()
        login_url = f"https://{device['ip']}/api/v1/authenticatedSession"
        headers = {"Content-Type": "application/json"}

        # Login
        res = session.post(login_url, json={
            "username": device["username"],
            "password": device["password"]
        }, headers=headers)

        if res.status_code != 200:
            raise Exception(f"Login failed: {res.status_code} {res.text}")

        # Example: Get firewall filtering rules as backup
        config_url = f"https://{device['ip']}/api/v1/firewallFilteringRules"
        response = session.get(config_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve config: {response.status_code} {response.text}")

        file_path = f"{base_path}/{device['name']}_{now}.json"
        with open(file_path, 'w') as f:
            f.write(response.text)

        print(f"[✓] Zscaler backup saved to {file_path}")

    except Exception as e:
        print(f"[!] Zscaler backup failed: {e}")
