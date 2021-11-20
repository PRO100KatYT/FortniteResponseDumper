import json
import requests
import os
from datetime import datetime

# The profiles that we will be requesting.
profiles = [
    "athena",
    "campaign",
    "collection_book_people0",
    "collection_book_schematics0",
    "collections",
    "common_core",
    "common_public",
    "metadata",
    "outpost0",
    "theater0"
]
# Links that will be used in the later part of code.
class links:
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/QueryProfile?profileId={1}"

def getAccessToken(req):
    # Getting the token and using it to login into an account.
    reqToken = req.post(
        links.getToken,
        headers={
            "Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=",
            "Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "token_type": "eg1",
            "code": input("Insert the auth code:\n")}).json()

    if "errorMessage" in reqToken:
        print(f"\nERROR: {reqToken['errorMessage']}")
        input("\nPress ENTER to close the program.\n")
        exit()
    access_token = reqToken["access_token"]
    account_id = reqToken["account_id"]
    displayName = reqToken["displayName"]
    print(f"Logged in as {displayName}.")
    return access_token, account_id, displayName

def Directories(displayName):
    # Creating Directories.
    path = os.path.join(
        os.path.split(
            os.path.abspath(__file__))[0],
        f"Dumped Profiles\\{displayName}\\{datetime.today().strftime('%Y-%m-%d %H-%M-%S')}")

    if not os.path.exists(path):
        os.makedirs(path)
    return path

def main():
    # Main func.
    print("Fortnite Profile Dumper v1.0.2 by PRO100KatYT & TeaDoc\n")
    req = requests.Session()
    access_token, account_id, displayName = getAccessToken(req)
    headers = {
        "Authorization": f"bearer {access_token}",
        "Content-Type": "application/json"
    }
    path = Directories(displayName)

    # Getting and dumping profiles
    for profile in profiles:
        SendReq(req, path, account_id, profile, headers)
    input(f"\nProfiles of {displayName} have been successfully dumped.\n\nPress ENTER to close the program.\n")

def SendReq(req, path, account_id, profile, headers):
    # Sending our request
    data = req.post(links.profileRequest.format(account_id, profile), headers=headers, data="{}").json()['profileChanges'][0]['profile']
    with open(f"{path}/{profile}.json", "w+") as file:
        file.write(json.dumps(data))
    print(f"Dumped the \"{profile}\" profile to {os.path.join(path, f'{profile}.json')}.")

if __name__ == "__main__":
    main()
