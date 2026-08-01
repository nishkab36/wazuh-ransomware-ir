from datetime import datetime, timedelta
from config import RULE_IDS, TIME_WINDOW
from datetime import timedelta
TIME_WINDOW = timedelta(seconds=TIME_WINDOW)
# Structure:
# {
#   "FLARE-VM": {
#       "110000": datetime(...),
#       "110001": datetime(...)
#   }
# }
agent_state = {}

def update_agent(agent_name, rule_id):
    """
    Store/update the latest timestamp for a rule observed on an agent.
    """

    now = datetime.now()

    if agent_name not in agent_state:
        agent_state[agent_name] = {}

    # Always update the rule
    agent_state[agent_name][rule_id] = now
    cleanup(agent_name)

def cleanup(agent_name):
    """
    Remove rules older than TIME_WINDOW.
    """
    now = datetime.now()
    expired = []

    for rule, ts in agent_state[agent_name].items():
        if now - ts > TIME_WINDOW:
            expired.append(rule)

    for rule in expired:
        del agent_state[agent_name][rule]

def check_correlation(agent_name):
    """
    Returns True only if all four ransomware rules
    have been observed within the time window.
    """

    if agent_name not in agent_state:
        return False

    return RULE_IDS.issubset(agent_state[agent_name].keys())

def reset_agent(agent_name):
    """
    Clear the stored state for an agent after a successful correlation.
    """

    if agent_name in agent_state:
        agent_state[agent_name].clear()
