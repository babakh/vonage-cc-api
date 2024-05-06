# vonage-cc-api

Vonage Contact Center (VCC) is a Contact Center as a Service (CCaaS) solution.  VCC offers a set of APIs that can be used for the following scenarios:
1) Automate user administration - instead of managing users/agents through VCC administration interface, you can use this API to create/update/detele users
2) Manage interaction data - you can use this API to access interaction data in real-time, extract and load the data into an enterprise repository for analytics or archiving, ...
3) Monitor agents - you may have a requirement to monitor agents for performance or workforce management
4) External application integration - You may have a requirement to initiate an interaction from an external application or receive notifications from VCC events in an external application
5) ...

For information on all the available APIs, please refer to the following: https://docs-vcc.atlassian.net/wiki/spaces/VCCA/overview

This is a basic Python v3 script to show you how to get started with VCC APIs.  It shows how to list users and download interaction data.  You can extend it for your usecase. 

Please note the following before running the script:
* Before you start, you need to configure an API Credential in VCC Admin Portal with the right scope(s) for the endpoints that you need.
* The sample code uses two environment variables for API Credentials: VONAGE_CLIENT_ID and VONAGE_SECRET.   After you create the API Credential, make sure to set these variables.
* The sample code uses nam as the region.  If your instance is in a different region, change accordingly.
* The script doesn't handle multi-page responses.
  <br />When you call the API, the response is in the following format: {'items': [], 'meta': {'pageCount': 0, 'totalCount': 0, 'page': 1, 'count': 0}}
 <br /> You'll need to check the pageCount and iterate through the pages. 
* The script downloads only last week's data.  When using /interactions, you must pass start and end times: https://docs-vcc.atlassian.net/wiki/spaces/VCCA/pages/3567190597/Search+for+interactions
  <br />As indicated, this can't exceed 7 days.  If you require different intervals, please change accordingly.
* Make sure to have installed the following packages in your Python enironment:
  <br />pip install requests
  <br />pip install pandas
* You can run the script as follows:
  <br />python vcc_script.py --operation list_users
  <br />python vcc_script.py --operation download_interactions 
