from atlassian import ServiceDesk

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json


# TODO: Replace Service Desk URL with the url of your JIRA service desk instance.
# TODO: Replace username and password with JIRA Service Desk username and password.
sd = ServiceDesk(
    url='https://example-desk.atlassian.net/',
    username='username',
    password='password')




def get_sd_id():
    return sd.get_service_desks()[1]["id"]

def create_request(values: dict, requestForEmail: str):
    
    # For more information on the information requried for this API call look at the Usage section of the README
    return sd.create_customer_request(get_sd_id(), "9", values, requestForEmail)

