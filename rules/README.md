# Custom Wazuh Detection Rules
This directory contains the custom Wazuh rules developed for detecting ransomware preparation behaviors on Windows endpoints.

## Rule Overview
| Rule ID | Behavior Detected |
|---------:|-------------------|
| 110000 | Volume Shadow Copy deletion using VSSAdmin |
| 110001 | Windows Backup Catalog deletion using WBAdmin |
| 110002 | Windows Recovery Environment disabled using BCDEdit |
| 110003 | Windows Event Log clearing using Wevtutil |

## Deployment
Copy the custom rules into the Wazuh manager's `local_rules.xml` file and restart the Wazuh manager for the changes to take effect.

## Purpose
These rules provide the event stream consumed by the Python correlation engine. Individually, each behavior may occur during legitimate administration; together, they indicate high-confidence ransomware preparation activity when correlated within the configured time window.
