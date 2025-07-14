[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

# 🔐 multi-vendor-firewalls-config-backup-and-batch-routing

A Python-based tool to **automate configuration backups** and **push batch interface and route configurations** across a wide range of firewall and network devices using SSH and REST APIs.

This tool enables both CLI-based and API-based backups, as well as simplified provisioning of network interfaces and static routes from structured YAML files.

---

## ✅ Supported Vendors

### 🔧 Batch Configuration Support (Interfaces & Routes via CLI)
- **Palo Alto** (SSH)
- **Cisco ASA / Firepower** (SSH)
- **Fortinet FortiGate** (SSH)
- **Juniper** (SSH)
- **Checkpoint Gaia CLI** (SSH)

### 🧾 Configuration Backup Support (CLI & API)
- **All of the above**, plus:
- **pfSense** (SSH)
- **F5 BIG-IP** (SSH/API)
- **Zscaler ZIA/ZPA** (API-based backup only)
- **Infoblox DDI** (API-based backup only)

---

## 📂 Project Structure

multi-vendor-firewalls-config-backup-and-batch-routing/
├── backups/ # Output folder for saved backup files
├── config/
│ ├── devices.yaml # Device inventory with IPs, credentials, and device types
│ └── push_config.yaml # CLI commands for batch interface & route configuration
├── modules/
│ ├── backup_checkpoint.py # API-based backup for Checkpoint firewalls
│ ├── backup_infoblox.py # API-based backup for Infoblox DNS/DHCP
│ └── backup_zscaler.py # API-based backup for Zscaler ZIA/ZPA
├── backup_firewalls.py # Main script to trigger configuration backups
├── push_configs.py # Script to push interface & route configs to CLI-based devices
└── README.md # Project documentation

---

## 🚀 Usage

### 1. Backup Configurations

- Update `config/devices.yaml` with your actual device information (IP, username, password, type).
- Run the backup script:

```bash
python backup_firewalls.py
