#!/usr/bin/env python3
from state import update_agent, check_correlation, agent_state, reset_agent
import subprocess
import json
import logging
from playbook import launch_playbook
from config import RULE_IDS

logging.basicConfig(
    filename="logs/correlator.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

cmd = [
    "sudo",
    "docker",
    "exec",
    "single-node_wazuh.manager_1",
    "tail",
    "-n",
    "0",
    "-F",
    "/var/ossec/logs/alerts/alerts.json"
]

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True

)

print("[+] Monitoring Wazuh alerts...\n")

logging.info("Started monitoring Wazuh alerts")

for line in process.stdout:

    try:
        alert = json.loads(line)
        rule = alert.get("rule", {})
        agent = alert.get("agent", {})

        rule_id = str(rule.get("id", ""))
        rule_desc = rule.get("description", "")
        agent_name = agent.get("name", "Unknown")

        if rule_id in RULE_IDS:
            update_agent(agent_name, rule_id)
            print("=" * 60)
            print(f"Agent       : {agent_name}")
            print(f"Rule ID     : {rule_id}")
            print(f"Description : {rule_desc}")
            print("=" * 60)
            logging.info(   f"Rule detected | Agent={agent_name} Rule={rule_id} Description={rule_desc}")

            if check_correlation(agent_name):
                print("\n" + "=" * 60)
                print(" HIGH CONFIDENCE RANSOMWARE DETECTED ")
                print(f" Host : {agent_name}")
                print("=" * 60 + "\n")
                logging.warning( f"High confidence ransomware detected on {agent_name}")
                logging.info(f"Launching playbook for {agent_name}")
                launch_playbook(agent_name, RULE_IDS)
                reset_agent(agent_name)


    except json.JSONDecodeError:
        continue
 
