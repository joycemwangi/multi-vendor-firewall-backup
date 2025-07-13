"""
push_configs.py

Batch configuration push tool for multi-vendor firewalls and network devices.

- Reads device details from config/devices.yaml
- Reads vendor-specific CLI commands from config/push_config.yaml
- Sends commands via SSH using Netmiko

Supports:
  - Palo Alto (PAN-OS)
  - Fortinet (FortiGate)
  - Cisco ASA
  - Juniper
  - Checkpoint Gaia

Note: Always review and test commands in a lab before deploying to production.
"""

import yaml
from netmiko import ConnectHandler
import os
import datetime

def load_yaml(file_path):
    with open(file_path) as f:
        return yaml.safe_load(f)

def push_config_to_device(device, config_commands):
    try:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = f"{log_dir}/{device['name']}_{now}.log"

        conn = ConnectHandler(
            device_type=device["type"],
            ip=device["ip"],
            username=device["username"],
            password=device["password"]
        )

        output = conn.send_config_set(config_commands)
        conn.save_config() if hasattr(conn, 'save_config') else None
        conn.disconnect()

        with open(log_file, 'w') as f:
            f.write(output)

        print(f"[✓] Config pushed to {device['name']} and logged to {log_file}")

    except Exception as e:
        print(f"[!] Failed to push config to {device['name']}: {e}")

def main():
    devices = load_yaml('config/devices.yaml')['devices']
    configs = load_yaml('config/push_config.yaml')['configs']

    for device in devices:
        device_type = device["type"]
        if device_type in configs:
            print(f"🔁 Pushing config to {device['name']} ({device_type})")
            push_config_to_device(device, configs[device_type])
        else:
            print(f"[!] No config found for {device['name']} ({device_type})")

if __name__ == "__main__":
    main()
