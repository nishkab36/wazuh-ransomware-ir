from pathlib import Path
from isolation import isolate_endpoint
from datetime import datetime
import logging
import json

def launch_playbook(agent_name, rules):
    timestamp = datetime.now()
    incident_id = timestamp.strftime("%Y%m%d-%H%M%S")
    folder_name = timestamp.strftime("%Y-%m-%d_%H-%M-%S") + "_" + agent_name
    incident_dir = Path("incidents") / folder_name
    incident_dir.mkdir(parents=True, exist_ok=True)
    summary = f"""Incident ID : {incident_id}

Host : {agent_name}
Severity : Critical
Detection Method :
Custom Python Correlation Engine
Observed Rules:
"""
    for rule in sorted(rules):
        summary += f"  - {rule}\n"

    summary += """

MITRE ATT&CK:
  - T1490
  - T1070.001
Status:
Playbook started.
"""
    (incident_dir / "summary.txt").write_text(summary)
    timeline = ""

    for rule in sorted(rules):
        timeline += f"{rule}\n"
    (incident_dir / "timeline.txt").write_text(timeline)

    incident = {
        "incident_id": incident_id,
        "host": agent_name,
        "severity": "Critical",
        "rules": sorted(list(rules)),
        "mitre": [
            "T1490",
            "T1070.001"
        ],
        "timestamp": timestamp.isoformat()
    }

    with open(incident_dir / "incident.json", "w") as f:
        json.dump(incident, f, indent=4)

    (incident_dir / "response.log").write_text(
        "Playbook started.\n"
    )

    print(f"[+] Incident package created: {incident_dir}")
    logging.info(f"Incident package created: {incident_dir}")
    print("[+] Initiating endpoint isolation...")
    logging.info("Initiating endpoint isolation")
    isolate_endpoint()
