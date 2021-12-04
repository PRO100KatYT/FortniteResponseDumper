print("Fortnite Profile Dumper v1.1.0 by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from datetime import datetime
    import webbrowser
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId=ec684b8c687f479fadea3cb2ad83f5c6&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253Dec684b8c687f479fadea3cb2ad83f5c6%2526responseType%253Dcode"
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId={2}"

# Getting the token and using it to login into an account.
isLoggedIn = input("Are you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n")
while True:
    if (isLoggedIn == "1" or isLoggedIn == "2"): break
    else: isLoggedIn = input("\nYou priovided a wrong value. Please input it again.\n")
input("\nThe program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
if isLoggedIn == "1": loginLink = links.loginLink1
else: loginLink = links.loginLink2
webbrowser.open_new_tab(loginLink)
print(f"If the program didnt open it, copy this link to your browser: {loginLink}\n")
reqToken = requests.post(links.getToken, headers={"Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=", "Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "authorization_code", "token_type": "eg1", "code": input("Insert the auth code:\n")})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    print(f"\nERROR: {reqTokenText['errorMessage']}")
    input("\nPress ENTER to close the program.\n") 
    exit()
else:
    access_token = reqTokenText["access_token"]
    account_id = reqTokenText["account_id"]
    displayName = reqTokenText["displayName"]
    print(f"\nLogged in as {displayName}.\n")

# Getting and dumping profiles.
path = os.path.join(os.path.split(os.path.abspath(__file__))[0], f"Dumped Profiles\{displayName}\{datetime.today().strftime('%Y-%m-%d %H-%M-%S')}")
if not os.path.exists(path): os.makedirs(path)
headers = {"Authorization": f"bearer {access_token}", "Content-Type": "application/json"}
profiles = ["athena", "campaign", "collection_book_people0", "collection_book_schematics0", "collections", "common_core", "common_public", "creative", "metadata", "outpost0", "theater0"]
profileCount = 0
while True:
    if profileCount > 10: break
    else:
        reqGetProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", profiles[profileCount]), headers=headers, data="{}")
        reqGetProfileText = json.loads(reqGetProfile.text)
        if "errorMessage" in reqGetProfileText:
            print(f"ERROR: {reqGetProfileText['errorMessage']}")
            input("\nPress ENTER to close the program.\n") 
            exit()
        json.dump(reqGetProfileText['profileChanges'][0]['profile'], open(os.path.join(path, f"{profiles[profileCount]}.json"), "w"), indent = 2)
        print(f"Dumped the {profiles[profileCount]} profile to {os.path.join(path, f'{profiles[profileCount]}.json')}.")
        profileCount += 1
input(f"\nProfiles of {displayName} have been successfully dumped.\n\nPress ENTER to close the program.\n")
exit()