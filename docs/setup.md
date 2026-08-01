# Project Setup Guide

This document describes how to recreate the project environment and execute the automated ransomware detection and response workflow.

> **Note**
> This project was developed and validated in a controlled virtual lab environment. Do **not** run the ransomware simulation commands on production systems.

---
# Prerequisites

## Host Environment

* Ubuntu 24.04 LTS
* Docker
* Python 3
* Git

## Security Platform

* Wazuh Manager 4.9
* Wazuh Dashboard

## Endpoint

* Windows 10 (FLARE-VM)
* Sysmon
* Wazuh Agent
* WinRM enabled

---
# Clone the Repository

```bash
git clone https://github.com/nishkab36/wazuh-ransomware-ir.git
cd wazuh-ransomware-ir
```

---
# Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---
# Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---
# Configure Wazuh

Copy the custom detection rules:
```
rules/local_rules.xml
```

to:
```
/var/ossec/etc/rules/local_rules.xml
```
Restart the Wazuh Manager after updating the rules.

---
# Configure the Endpoint

Verify that the Windows endpoint has:

* Sysmon installed
* Wazuh Agent connected
* WinRM enabled
* Administrative credentials configured for remote isolation

---
# Verify Telemetry

Before testing, confirm that:

* Sysmon Process Creation events are generated.
* The Wazuh Agent forwards telemetry.
* Events appear in the Wazuh Dashboard.
* The custom detection rules trigger successfully.

---
# Run the Correlation Engine

Activate the virtual environment:
```bash
source venv/bin/activate
```

Start the correlation engine:
```bash
python src/correlator.py
```

---
# Execute the Demonstration

Run the ransomware preparation commands on the Windows endpoint.

The demonstration simulates:

* Volume Shadow Copy deletion
* Windows Backup Catalog deletion
* Windows Recovery modification
* Windows Event Log clearing

After all four behaviors are detected within the configured correlation window, the framework will:

1. Generate a high-confidence ransomware detection.
2. Create an incident package.
3. Connect to the endpoint using WinRM.
4. Disable the active network adapter.
5. Isolate the endpoint.
6. Confirm the Wazuh Agent is disconnected.

---
# Expected Output

A successful execution generates:
```text
docs/sample-output/
├── incident.json
├── response.log
├── summary.txt
└── timeline.txt
```

---
# Troubleshooting

## Python Module Errors

Reinstall the project dependencies:
```bash
pip install -r requirements.txt
```

## WinRM Connection Issues

Verify that:

* WinRM is enabled.
* The endpoint is reachable.
* The configured credentials are correct.
* Firewall rules allow WinRM connections.

## No Detection Generated

Verify that:

* Sysmon is generating telemetry.
* The Wazuh Agent is connected.
* The custom detection rules are loaded.
* The correlation engine is running.
* All four ransomware preparation behaviors occur within the configured correlation window.
