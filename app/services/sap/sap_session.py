import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Disable SSL warnings (yellow warning fix)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SAP_BASE_URL = os.getenv("SAP_BASE_URL")
SAP_USERNAME = os.getenv("SAP_USERNAME")
SAP_PASSWORD = os.getenv("SAP_PASSWORD")

sap_session = requests.Session()
sap_session.auth = HTTPBasicAuth(SAP_USERNAME, SAP_PASSWORD)
sap_session.headers.update({
    "Accept": "application/json"
})

# IMPORTANT: SAP internal cert → disable SSL verify
sap_session.verify = False
sap_session.timeout = 30
