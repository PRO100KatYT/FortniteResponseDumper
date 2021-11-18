import json
import requests
import os
from datetime import datetime

# Links that will be used in the later part of code.
class links:
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId={2}"

print("Fortnite Profile Dumper v1.0.1 by PRO100KatYT\n")

# Getting the token and using it to login into an account.
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
reqGetAthenaProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "athena"), headers=headers, data="{}")
json.dump(json.loads(reqGetAthenaProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "athena.json"), "w"), indent = 2)
print(f"Dumped the athena profile to {os.path.join(path, 'athena.json')}.")
reqGetCampaignProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "campaign"), headers=headers, data="{}")
json.dump(json.loads(reqGetCampaignProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "campaign.json"), "w"), indent = 2)
print(f"Dumped the campaign profile to {os.path.join(path, 'campaign.json')}.")
reqGetCollectionBookPeopleProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "collection_book_people0"), headers=headers, data="{}")
json.dump(json.loads(reqGetCollectionBookPeopleProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "collection_book_people0.json"), "w"), indent = 2)
print(f"Dumped the collection_book_people0 profile to {os.path.join(path, 'collection_book_people0.json')}.")
reqGetCollectionBookSchematicsProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "collection_book_schematics0"), headers=headers, data="{}")
json.dump(json.loads(reqGetCollectionBookSchematicsProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "collection_book_schematics0.json"), "w"), indent = 2)
print(f"Dumped the collection_book_schematics0 profile to {os.path.join(path, 'collection_book_schematics0.json')}.")
reqGetCollectionsProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "collections"), headers=headers, data="{}")
json.dump(json.loads(reqGetCollectionsProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "collections.json"), "w"), indent = 2)
print(f"Dumped the collections profile to {os.path.join(path, 'collections.json')}.")
reqGetCommonCoreProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "common_core"), headers=headers, data="{}")
json.dump(json.loads(reqGetCommonCoreProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "common_core.json"), "w"), indent = 2)
print(f"Dumped the common_core profile to {os.path.join(path, 'common_core.json')}.")
reqGetCommonPublicProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "common_public"), headers=headers, data="{}")
json.dump(json.loads(reqGetCommonPublicProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "common_public.json"), "w"), indent = 2)
print(f"Dumped the common_public profile to {os.path.join(path, 'common_public.json')}.")
reqGetCreativeProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "creative"), headers=headers, data="{}")
json.dump(json.loads(reqGetCreativeProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "creative.json"), "w"), indent = 2)
print(f"Dumped the creative profile to {os.path.join(path, 'creative.json')}.")
reqGetMetadataProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "metadata"), headers=headers, data="{}")
json.dump(json.loads(reqGetMetadataProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "metadata.json"), "w"), indent = 2)
print(f"Dumped the metadata profile to {os.path.join(path, 'metadata.json')}.")
reqGetOutpostProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "outpost0"), headers=headers, data="{}")
json.dump(json.loads(reqGetOutpostProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "outpost0.json"), "w"), indent = 2)
print(f"Dumped the outpost0 profile to {os.path.join(path, 'outpost0.json')}.")
reqGetTheaterProfile = requests.post(links.profileRequest.format(account_id, "QueryProfile", "theater0"), headers=headers, data="{}")
json.dump(json.loads(reqGetTheaterProfile.text)['profileChanges'][0]['profile'], open(os.path.join(path, "theater0.json"), "w"), indent = 2)
print(f"Dumped the theater0 profile to {os.path.join(path, 'theater0.json')}.")
input(f"\nProfiles of {displayName} have been successfully dumped.\n\nPress ENTER to close the program.\n")
exit()