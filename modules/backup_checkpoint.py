"""
backup_checkpoint.py

Module to perform automated backups of Checkpoint firewalls
using Checkpoint Management API.

Prerequisites:
- Checkpoint management IP and API credentials configured in devices.yaml
- Python requests module installed
- API user with appropriate permissions to fetch configurations

Usage:
- Called internally by backup_firewalls.py
- Adjust API version, login endpoints, or commands as needed

Note:
- SSL verification can be adjusted (verify=False) if self-signed certificates are used
- Replace placeholders with actual IP, username, and password in devices.yaml
"""

import requests
import os
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def backup_checkpoint(device):
    try:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_path = 'backups/checkpoint'
        os.makedirs(base_path, exist_ok=True)

        session = requests.Session()
        login_url = f"https://{device['ip']}/web_api/login"

        payload = {
            "user": device["username"],
            "password": device["password"]
        }

        response = session.post(login_url, json=payload, verify=False)
        if response.status_code != 200:
            raise Exception(f"Checkpoint login failed: {response.status_code} {response.text}")

        sid = response.json().get("sid")
        if not sid:
            raise Exception("No session ID received")

        headers = {"X-chkp-sid": sid}

        # Example API call: list gateways and servers (modify as needed)
        config_url = f"https://{device['ip']}/web_api/show-gateways-and-servers"
        config_res = session.post(config_url, headers=headers, verify=False)

        if config_res.status_code != 200:
            raise Exception(f"Failed to get configuration: {config_res.status_code} {config_res.text}")

        file_path = f"{base_path}/{device['name']}_{now}.json"
        with open(file_path, 'w') as f:
            f.write(config_res.text)

        # Logout
        session.post(f"https://{device['ip']}/web_api/logout", headers=headers, verify=False)

        print(f"[✓] Checkpoint backup saved to {file_path}")

    except Exception as e:
        print(f"[!] Checkpoint backup failed: {e}")
