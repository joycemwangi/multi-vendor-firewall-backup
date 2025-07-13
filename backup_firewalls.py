"""
backup_firewalls.py
-------------------

Automated backup script for multi-vendor firewalls and network devices using SSH and APIs.

NOTE:
- Update `config/devices.yaml` with actual device IPs and credentials.
- Ensure required Python modules are installed: netmiko, pyyaml, requests.
- Some devices may require custom modules (see modules/ folder).
"""

import yaml
from netmiko import ConnectHandler
import datetime
import os

# Import API-based modules
from modules.backup_zscaler import backup_zscaler
from modules.backup_infoblox import backup_infoblox
from modules.backup_checkpoint import backup_checkpoint

def load_devices(file_path='config/devices.yaml'):
    with open(file_path) as f:
        return yaml.safe_load(f)['devices']

def ssh_backup(device):
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_path = f'backups/{device["type"]}'
    os.makedirs(base_path, exist_ok=True)

    try:
        conn = ConnectHandler(
            device_type=device["type"],
            ip=device["ip"],
            username=device["username"],
            password=device["password"]
        )

        # SSH-based commands by vendor
        if device["type"] in ["cisco_asa", "cisco_ios"]:
    
# Cisco ASA or IOS devices - fetch running config via SSH
            output = conn.send_command("show running-config")
        elif device["type"] == "juniper":
    # Juniper devices - fetch config in set format
            output = conn.send_command("show configuration | display set")
        elif device["type"] == "fortinet":
            output = conn.send_command("show full-configuration")
        elif device["type"] == "paloalto_panos":
            output = conn.send_command("show config running")
        elif device["type"] == "pfsense":
            output = conn.send_command("cat /cf/conf/config.xml")
        elif device["type"] == "f5":
            output = conn.send_command("tmsh list /sys config")
        elif device["type"] == "checkpoint_cli":
            output = conn.send_command("show configuration")
        else:
            output = f"{device['name']} is not supported for SSH backup."

        filename = f"{base_path}/{device['name']}_{now}.txt"
        with open(filename, 'w') as f:
            f.write(output)

        print(f"[✓] Backup saved for {device['name']} at {filename}")
        conn.disconnect()

    except Exception as e:
        print(f"[!] Error backing up {device['name']} via SSH: {e}")

def backup_device(device):
    # Determine backup method based on device type
    if device["type"] == "zscaler":
        backup_zscaler(device)
    elif device["type"] == "infoblox":
        backup_infoblox(device)
    elif device["type"] == "checkpoint":
        backup_checkpoint(device)
    else:
        ssh_backup(device)

def main():
    devices = load_devices()
    for device in devices:
        print(f"🔄 Backing up {device['name']} ({device['type']})")
        backup_device(device)

if __name__ == "__main__":
    main()
