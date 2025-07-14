[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

# 🔐 multi-vendor-firewall-backup

Automated configuration backups and batch interface & route configuration for firewalls and network devices using Python, SSH, and REST APIs.

This tool supports multiple vendors and provides modular backup functions for CLI-based and API-based devices, as well as automated deployment of interface and routing configurations.

Supported devices for configuration pushing include:
- Palo Alto
- Fortinet FortiGate
- Cisco ASA and Firepower
- Juniper
- Checkpoint Gaia

Configuration commands are defined in a YAML file and applied via the `push_configs.py` script.

---

## ✅ Supported Vendors

- **Palo Alto** (SSH/API)
- **Cisco ASA / Firepower** (SSH/API)
- **Fortinet** (SSH)
- **Juniper** (SSH)
- **Checkpoint** (SmartConsole API)
- **pfSense** (SSH)
- **F5 BIG-IP** (SSH/API)
- **Zscaler ZIA/ZPA** (API)
- **Infoblox** (WAPI REST API)

---

## 📂 Project Structure

multi-vendor-firewall-backup/
├── backups/                # Output folder for saved backup files
├── config/
│   ├── devices.yaml        # Device inventory with IPs, credentials, and types
│   └── push_config.yaml    # CLI commands for batch interface & route configuration
├── modules/
│   ├── backup_checkpoint.py  # API-based backup for Checkpoint firewalls
│   ├── backup_infoblox.py    # API-based backup for Infoblox DNS/DHCP
│   └── backup_zscaler.py     # API-based backup for Zscaler
├── backup_firewalls.py      # Main script to trigger configuration backups
├── push_configs.py          # Script to push interface & route configs to devices
└── README.md                # Project documentation

---

## 🚀 Usage

1. **Backup Configurations**

   Update your device details in `config/devices.yaml`.

   Run the backup script:

   ```bash
   python backup_firewalls.py
