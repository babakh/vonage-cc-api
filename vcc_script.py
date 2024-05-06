import os, logging, requests, json, argparse
from datetime import datetime, timedelta
from pandas import DataFrame

SCOPE_AGENT_AVAILABILITY         = "agents-availability:read"
SCOPE_READ_USERS                 = "users:read"
SCOPE_WRITE_USERS                = "users:write"
SCOPE_INTERACTION_CONTENT_READ   = "interaction-content:read"
SCOPE_INTERACTION_CONTENT_DELETE = "interaction-content:delete"
SCOPE_INTERACTION_WRITE          = "interactions:write"

client_id     = os.environ['VONAGE_CLIENT_ID']
client_secret = os.environ['VONAGE_SECRET']

auth_url  = "https://nam.newvoicemedia.com"     # replace nam with your region
api_url   = "https://nam.api.newvoicemedia.com" # replace nam with your region

grant_type = "client_credentials"

time_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=time_format)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def authenticate(scope):
    auth_header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
    "grant_type" : grant_type, 
    "client_id" : client_id, 
    "client_secret" : client_secret,
    "scope" : scope 
    }
    
    url = auth_url + "/Auth/connect/token" 

    resp = requests.post(url, headers=auth_header, data=data)

    if resp.status_code == 200:
        response = json.loads(resp.text)
        return response["access_token"]
    else:
        logging.error("{} - {}".format(resp.status_code, resp.text))
        return

def get_users():
    users_list = []
    logging.info("Retrieving users from VCC")
    token = authenticate(SCOPE_READ_USERS)
    headers = {"Authorization": "Bearer " + token}
    url = api_url + "/useradmin/users"
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        users = json.loads(resp.text)
        for user in users:
            users_list.append(user)
        filename= datetime.now().strftime("%m_%d_%Y-%H_%M_%S") + '-vcc_users.csv'
        df = DataFrame(users_list)
        df.to_csv(filename, sep=',', index=False, encoding='utf-8')
        logging.info('Extracted {:,} users from VCC, and wrote the data to {}'.format(len(users_list), filename))
    else:
        logging.error("{} - {}".format(resp.status_code, resp.text))
        

def get_interactions(start_time, end_time):
    interactions_list = []
    logging.info("Retrieving interactions from {} to {}".format(start_time, end_time))
    token = authenticate(SCOPE_INTERACTION_CONTENT_READ)
    headers = {
        "Authorization": "Bearer " + token,
        "Accept" : "application/vnd.newvoicemedia.v2+json"
    }
               
    url = api_url + "/interaction-content/interactions"
    url +="?start=" + start_time.isoformat() + "Z"
    url +="&end="   + end_time.isoformat() + "Z"
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        interactions = json.loads(resp.text)
        for interaction in interactions['items']:
            interactions_list.append(interaction)
        filename= datetime.now().strftime("%m_%d_%Y-%H_%M_%S") + '-vcc_interactions.csv'
        df = DataFrame(interactions_list)
        df.to_csv(filename, sep=',', index=False, encoding='utf-8')
        logging.info('Extracted {:,} interactions from VCC, and wrote the data to {}'.format(len(interactions_list), filename))
    else:
        logging.error(resp.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", choices=["list_users", "download_interactions"],  help="the operation to perform")

    args = parser.parse_args()

    if args.operation == "list_users":
        get_users()
    elif args.operation == "download_interactions":
        now = datetime.now()
        start_time = now + timedelta(weeks=-1) # let's grab the data for the last 7 days
        end_time   = now 
        get_interactions(start_time, end_time)