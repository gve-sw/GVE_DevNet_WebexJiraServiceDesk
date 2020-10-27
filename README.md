# GVE_DevNet_WebexJiraServiceDesk
A Webex Teams bot that is integrated with Jira Service Desk to create support tickets.



## Contacts
* Charles Llewellyn
*  Jason Mah

## Solution Components
* Webex Teams
*  Jira Service Desk

## Installation/Configuration

This is as a template, project owner to update

Add any steps needed to install the project so that someone can reproduce the project

```python
# app.py FILE:
# Change EXTERNAL_WEBHOOK_URL to the external server you want to receive from Webex Teams
EXTERNAL_WEBHOOK_URL = "34.16.23.56:8000"

# webex.py FILE:
# update the WEBEX_TEAMS_ACCESS_TOKEN with your Bot's webex teams bearer token.
WEBEX_TEAMS_ACCESS_TOKEN = "AFNCALKJ229XFAJANCKASHIFAHANCEXAMPLEBEAERERTOKEN1234"

# jira.py FILE:
# Replace Service Desk URL with the url of your JIRA service desk instance.
# Replace username and password with JIRA Service Desk username and password.
sd = ServiceDesk(
    url='https://example-desk.atlassian.net/',
    username='example',
    password='password123')


```


## Usage

### Jira.py usage (select desk):

    def get_sd_id():
        return sd.get_service_desks()[1]["id"]
        
In the get_sd_id() function, the [1] refers to the service desk that is being selected. Here it is the 2nd service desk available in the enviornment, which is the [Test Desk](/IMAGES/select-desk.png) in this example. 

If we used 
    
    sd.get_service_desks()[0]["id"] 

we would instead be submitting our ticket to the Demo desk seen in the above link.

        
___________________________________________________________________________________________________________________
### Jira.py usage (select Ticket(issue) type):

    def create_request(values: dict, requestForEmail: str):
            return sd.create_customer_request(get_sd_id(), "9", values, requestForEmail)

In sd.create_customer_request(), which is inside of create_request() function, the first input it takes is the id of the service-desk selected from get_sd_id(). The next input, "9" refers to the issue id. Here is how you find the issue ID:

1. Select your [Service Desk](/IMAGES/select-desk.png)
2. Click on [Raise a Request](/IMAGES/raise-issue.png) in the side-bar 
3. Select the type of Issue you would like to [raise](/IMAGES/select-issue.png)
4. Select the sub-issue that you would like to [raise](/IMAGES/select-sub-issue.png)
5. Look at the end of the URL on the [sub-issue](/IMAGES/create-issue.png), it should be a number, and that number is the issue-id. Please use that number to refer to the issue-id. In this example, the issue-id is "9".


The next input that sd.create_customer_request() takes is called values, which refers to the values that you would like to pass to the raised request. For example, you could have a dictionary with description and summary: 
    
    values = {"Description": "this is the description", "Summary": "This is the summary"}

Lastly, the requestForEmail variable is the email of the requestor.

### App usage
To launch an this program:


    $ python app.py



# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)
![/IMAGES/adaptive-card-template.png](/IMAGES/adaptive-card-template.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
