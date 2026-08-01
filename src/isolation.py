import winrm
import logging
from config import WINDOWS_HOST, USERNAME, PASSWORD

def isolate_endpoint():
    """
    Disable the active network adapter on the Windows endpoint.
    """

    session = winrm.Session(
        f"http://{WINDOWS_HOST}:5985/wsman",
        auth=(USERNAME, PASSWORD),
        transport="ntlm"
    )

    try:

        session.run_ps("""
        Disable-NetAdapter -Name "Ethernet0" -Confirm:$false
        """)
        print("[+] Isolation command sent successfully.")
        logging.info("Isolation command sent successfully")

    except Exception as e:

        if "Read timed out" in str(e):

            print("[+] Endpoint isolation completed.")
            logging.info("Endpoint isolation completed.")

        else:

            print(f"[!] Isolation failed: {e}")
            logging.error(f"Isolation failed: {e}")
