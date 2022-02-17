version = "1.3.2"
configVersion = "1.3.2"
print(f"Fortnite Response Dumper v{version} by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from configparser import ConfigParser
    from datetime import datetime
    import webbrowser
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId={0}&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D{0}%2526responseType%253Dcode"
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    singleResponses = {"Dump_Catalog": ["https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/storefront/v2/catalog", "{}", "Catalog (Item Shop)", "catalog"], "Dump_Keychain": ["https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/storefront/v2/keychain", "{}", "Keychain", "keychain"], "Dump_Contentpages": ["https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game" , "", "Contentpages (News)", "contentpages"], "Dump_Timeline": ["https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/calendar/v1/timeline", "{}", "Timeline", "timeline"], "Dump_Theater": ["https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/world/info", "{}", "Theater (StW World)", "worldstw"]}
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/QueryProfile?profileId={1}"
    friendlists = [["https://friends-public-service-prod06.ol.epicgames.com/friends/api/public/friends/{0}?includePending=true", "Friendslist #1", "friendslist"], ["https://friends-public-service-prod06.ol.epicgames.com/friends/api/v1/{0}/summary", "Friendslist #2", "friendslist2"]]
    friendsinfo = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account?{0}"
    cloudstorageRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/cloudstorage/{0}"

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"ERROR: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(f"You set the wrong {key} value in config.ini ({value}). Valid values: {validValues}. Please change it and run this program again.")

# Loop input until the response is one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if response in values: break
        response = input("You priovided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request, bJson):
    if bJson: requestText = json.loads(request.text)
    else: requestText = request.text
    if "errorMessage" in requestText: customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqTokenText(loginLink, authHeader):
    webbrowser.open_new_tab(loginLink)
    print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
    reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": f"basic {authHeader}"}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")}), True)
    return reqToken

# Round the file size.
def roundSize(filePathToSave):
    fileSize = round(os.path.getsize(filePathToSave)/1024, 1)
    if str(fileSize).endswith(".0"): fileSize = round(fileSize)
    return fileSize

# Create and/or read the config.ini file.
config, configPath = [ConfigParser(), os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")]
langValues, boolValues = [["de", "ru", "ko", "en", "it", "fr", "es", "ar", "ja", "pl", "es-419", "tr"], ["true", "false"]]
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n")
    bStartSetup = validInput("Type 1 if you want to start the config setup and press ENTER.\nType 2 if you want to use the default config values and press ENTER.", ["1", "2"])
    if bStartSetup == "1":
        iAuthorization_Type = validInput("Which authentication method do you want the program to use?\nToken auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\nDevice auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\nValid vaules: token, device.", ["token", "device"])
        iLanguage = validInput(f"What language do you want some of the saved responses to be?\nValid vaules: {', '.join(langValues)}", langValues)
        iList = []
        dumpOptionsJson = {"Dump_Catalog": "Catalog (Item Shop)", "Dump_Keychain": "Keychain", "Dump_Contentpages": "Contentpages (News)", "Dump_Timeline": "Timeline", "Dump_Theater": "Theater (StW World)", "Dump_Profiles": "Account Profiles", "Dump_Friendlists": "Epic Friends related responses", "Dump_Account_Cloudstorage": "Account Cloudstorage", "Dump_Global_Cloudstorage": "Global Cloudstorage"}
        for option in dumpOptionsJson: iList.append(validInput(f"Do you want the program to dump the {dumpOptionsJson[option]}?\nValid vaules: {', '.join(boolValues)}.", boolValues))
        iDump_Catalog, iDump_Keychain, iDump_Contentpages, iDump_Timeline, iDump_Theater, iDump_Profiles, iDump_Friendlists, iDump_Account_Cloudstorage, iDump_Global_Cloudstorage = iList
        iSave_Empty_Cloudstorage = validInput(f"Do you want the program to save Global Cloudstorage files that are empty?\nValid vaules: {', '.join(boolValues)}.", boolValues)
    else: iAuthorization_Type, iLanguage, iDump_Catalog, iDump_Keychain, iDump_Contentpages, iDump_Timeline, iDump_Theater, iDump_Profiles, iDump_Friendlists, iDump_Account_Cloudstorage, iDump_Global_Cloudstorage, iSave_Empty_Cloudstorage = ["token", "en", "true", "true", "true", "true", "true", "true", "true", "true", "true", "false"]
    with open(configPath, "w") as configFile: configFile.write(f"[Fortnite_Response_Dumper_Config]\n\n# Which authentication method do you want the program to use?\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\n# Valid vaules: token, device.\nAuthorization_Type = {iAuthorization_Type}\n\n# What language do you want some of the saved responses to be?\n# Valid vaules: de, ru, ko, en, it, fr, es, ar, ja, pl, es-419, tr.\nLanguage = {iLanguage}\n\n# Do you want the program to dump the Catalog (Item Shop)?\n# Valid vaules: true, false.\nDump_Catalog = {iDump_Catalog}\n\n# Do you want the program to dump the Keychain?\n# Valid vaules: true, false.\nDump_Keychain = {iDump_Keychain}\n\n# Do you want the program to dump the Contentpages (News)?\n# Valid vaules: true, false.\nDump_Contentpages = {iDump_Contentpages}\n\n# Do you want the program to dump the Timeline?\n# Valid vaules: true, false.\nDump_Timeline = {iDump_Timeline}\n\n# Do you want the program to dump the Theater (StW World)?\n# Valid vaules: true, false.\nDump_Theater = {iDump_Theater}\n\n# Do you want the program to dump the account profiles?\n# Valid vaules: true, false.\nDump_Profiles = {iDump_Profiles}\n\n# Do you want the program to dump the Epic Friends related responses?\n# Valid vaules: true, false.\nDump_Friendlists = {iDump_Friendlists}\n\n# Do you want the program to dump the account Cloudstorage?\n# Valid vaules: true, false.\nDump_Account_Cloudstorage = {iDump_Account_Cloudstorage}\n\n# Do you want the program to dump the global Cloudstorage?\n# Valid vaules: true, false.\nDump_Global_Cloudstorage = {iDump_Global_Cloudstorage}\n\n# Do you want the program to save Cloudstorage files that are empty?\n# Valid vaules: true, false.\nSave_Empty_Cloudstorage = {iSave_Empty_Cloudstorage}\n\n# Do not change anything below.\n[Config_Version]\nVersion = FRD_{configVersion}")
    print("The config.ini file was generated successfully.\n")
try:
    config.read(configPath)
    configVer, authType, lang, bDumpCatalog, bDumpKeychain, bDumpContentpages, bDumpTimeline, bDumpTheater, bDumpProfiles, bDumpFriendlists, bDumpAccountCloudstorage, bDumpGlobalCloudstorage, bSaveEmptyCloudstorage = [config['Config_Version']['Version'], config['Fortnite_Response_Dumper_Config']['Authorization_Type'].lower(), config['Fortnite_Response_Dumper_Config']['Language'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Catalog'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Keychain'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Contentpages'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Timeline'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Theater'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Profiles'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Friendlists'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Account_Cloudstorage'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Global_Cloudstorage'].lower(), config['Fortnite_Response_Dumper_Config']['Save_Empty_Cloudstorage'].lower()]
except:
    customError("The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
checkValuesJson, trueValues = [{"Authorization_Type": {"value": authType, "validValues": ["token", "device"]}, "Language": {"value": lang, "validValues": langValues}, "Dump_Catalog": {"value": bDumpCatalog, "validValues": boolValues}, "Dump_Keychain": {"value": bDumpKeychain, "validValues": boolValues}, "Dump_Contentpages": {"value": bDumpContentpages, "validValues": boolValues}, "Dump_Timeline": {"value": bDumpTimeline, "validValues": boolValues}, "Dump_Theater": {"value": bDumpTheater, "validValues": boolValues}, "Dump_Profiles": {"value": bDumpProfiles, "validValues": boolValues}, "Dump_Friendlists": {"value": bDumpFriendlists, "validValues": boolValues}, "Dump_Account_Cloudstorage": {"value": bDumpAccountCloudstorage, "validValues": boolValues}, "Dump_Global_Cloudstorage": {"value": bDumpGlobalCloudstorage, "validValues": boolValues}, "Save_Empty_Cloudstorage": {"value": bSaveEmptyCloudstorage, "validValues": boolValues}}, 0]
for option in checkValuesJson:
    if not (checkValuesJson[option]['value'] in checkValuesJson[option]['validValues']): customError(f"You set the wrong {option} value in config.ini ({checkValuesJson[option]['value']}). Valid values: {', '.join(checkValuesJson[option]['validValues'])}. Please change it and run this program again.")
    elif checkValuesJson[option]['value'] == "false": links.singleResponses.pop(option, None)
    else: trueValues += 1
if not (configVer == f"FRD_{configVersion}"): customError("The config file is outdated. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")

# Create and/or read the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    isLoggedIn = validInput("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
    input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
    if isLoggedIn == "1": loginLink = links.loginLink1
    else: loginLink = links.loginLink2
    if authType == "token":
        reqToken = reqTokenText(loginLink.format("34a02cf8f4414e29b15921876da36f9a"), "MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=")
        refreshToken, accountId, expirationDate = [reqToken["refresh_token"], reqToken["account_id"], reqToken["refresh_expires_at"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "refresh_expires_at": expirationDate}, authFile, indent = 2)
    else:
        reqToken = reqTokenText(loginLink.format("3446cd72694c4a4485d81b77adbb2141"), "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=")
        accessToken, accountId = [reqToken["access_token"], reqToken["account_id"]]
        reqDeviceAuth = requestText(session.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
        deviceId, secret = [reqDeviceAuth["deviceId"], reqDeviceAuth["secret"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "device",  "deviceId": deviceId, "accountId": accountId, "secret": secret}, authFile, indent = 2)
    print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    if authType == "token":
        if getAuthJson["authType"] == "device": customError("The authorization type in config is set to token, but the auth.json file contains device auth credentials.\nDelete the auth.json file and run this program again to generate a token one or change authorization type back to device in config.ini.")
        expirationDate, refreshToken = [getAuthJson["refresh_expires_at"], getAuthJson["refreshToken"]]
        if expirationDate < datetime.now().isoformat(): customError("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one.")
    if authType == "device":
        if getAuthJson["authType"] == "token": customError("The authorization type in config is set to device, but the auth.json file contains token auth credentials.\nDelete the auth.json file and run this program again to generate a device one or change authorization type back to token in config.ini.")
        deviceId, secret = [getAuthJson["deviceId"], getAuthJson["secret"]]
    accountId = getAuthJson["accountId"]
except:
    customError("The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.")

# Log in.
if authType == "token": # Shoutout to BayGamerYT for telling me about this login method.
    reqRefreshToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), True)
    with open(authPath, "r") as getAuthFile: authFile = json.loads(getAuthFile.read())
    authFile['refreshToken'], authFile['refresh_expires_at'] = [reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]]
    with open(authPath, "w") as getAuthFile: json.dump(authFile, getAuthFile, indent = 2)
    reqExchange = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
    reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
if authType == "device": reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
accessToken, displayName = [reqToken['access_token'], reqToken['displayName']]
print(f"Logged in as {displayName}.\n")

if bDumpCatalog == bDumpKeychain == bDumpContentpages == bDumpTimeline == bDumpTheater == bDumpProfiles == bDumpFriendlists == bDumpAccountCloudstorage == bDumpGlobalCloudstorage == "false": print(f"You set everything the program can save to false in the config. Why are we still here? Just to suffer?\n")
headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json", "X-EpicGames-Language": lang, "Accept-Language": lang}

currentDate = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
path = os.path.join(os.path.split(os.path.abspath(__file__))[0], "Dumped files")
path = os.path.join(path, f"{currentDate}")
if not os.path.exists(path): os.makedirs(path)

# Get and dump single responses.
responseCount = 0
for response in links.singleResponses:
    reqGetResponseText = requestText(session.get(links.singleResponses[response][0], headers=headers, data=links.singleResponses[response][1]), True)
    filePathToSave = os.path.join(path, f"{links.singleResponses[response][3]}.json")
    with open(filePathToSave, "w", encoding = "utf-8") as fileToSave: json.dump(reqGetResponseText, fileToSave, indent = 2, ensure_ascii = False)
    fileSize = roundSize(filePathToSave)
    print(f"Dumped the {links.singleResponses[response][2]} ({fileSize} KB) to {filePathToSave}.\n")
    responseCount += 1

# Get and dump the profiles.
if bDumpProfiles == "true":
    profilePath = os.path.join(path, f"{displayName}'s Profiles")
    if not os.path.exists(profilePath): os.makedirs(profilePath)
    profiles = ["athena", "campaign", "collection_book_people0", "collection_book_schematics0", "collections", "common_core", "common_public", "creative", "metadata", "outpost0", "recycle_bin", "theater0", "theater1", "theater2"]
    print(f"Starting to dump {len(profiles)} {displayName}'s profiles")
    profileCount = 0
    for profileId in profiles:
        reqGetProfileText = requestText(session.post(links.profileRequest.format(accountId, profileId), headers=headers, data="{}"), True)
        profileFilePath = os.path.join(profilePath, f"{profileId}.json")
        with open(profileFilePath, "w") as fileToSave: json.dump(reqGetProfileText['profileChanges'][0]['profile'], fileToSave, indent = 2)
        fileSize = roundSize(profileFilePath)
        profileCount += 1
        print(f"{profileCount}: Dumped the {profileId} profile ({fileSize} KB)")
    print(f"\n{displayName}'s profiles have been successfully saved in {profilePath}.\n")

# Get and dump the Epic Friends related responses.
if bDumpFriendlists == "true":
    friendsPath = os.path.join(path, f"{displayName}'s Friends")
    if not os.path.exists(friendsPath): os.makedirs(friendsPath)
    for friendslist in links.friendlists:
        reqGetFriendslistText = requestText(session.get(friendslist[0].format(accountId), headers=headers, data="{}"), True)
        friendslistFilePath = os.path.join(friendsPath, f"{friendslist[2]}.json")
        with open(friendslistFilePath, "w") as fileToSave: json.dump(reqGetFriendslistText, fileToSave, indent = 2)
        fileSize = roundSize(friendslistFilePath)
        print(f"Dumped the {friendslist[2]} ({fileSize} KB)\n")
    friendAccountIds = ""
    for friend in reqGetFriendslistText['friends']:
        if friendAccountIds != "": friendAccountIds += "&"
        friendAccountIds += f"accountId={friend['accountId']}"
    reqGetFriendsInfoText = requestText(session.get(links.friendsinfo.format(friendAccountIds), headers=headers, data="{}"), True)
    friendsInfoFilePath = os.path.join(friendsPath, f"friendsinfo.json")
    with open(friendsInfoFilePath, "w") as fileToSave: json.dump(reqGetFriendsInfoText, fileToSave, indent = 2)
    fileSize = roundSize(friendsInfoFilePath)
    print(f"Dumped the Friends Info ({fileSize} KB)\n\n{displayName}'s Epic Friends responses have been successfully saved in {friendsPath}.\n")


# Get and dump the account Cloudstorage.
if bDumpAccountCloudstorage == "true":
    userCSPath = os.path.join(path, f"{displayName}'s Cloudstorage")
    if not os.path.exists(userCSPath): os.makedirs(userCSPath)
    reqGetCloudstorageText = requestText(session.get(links.cloudstorageRequest.format(f"user/{accountId}"), headers=headers, data="{}"), True)
    cloudstorageIDList,  cloudstorageNameList, cloudstorageCount = [[], [], 0]
    for key in reqGetCloudstorageText:
        cloudstorageIDList.append(key['uniqueFilename'])
        cloudstorageNameList.append(key['filename'])
    print(f"Starting to dump {len(cloudstorageIDList)} {displayName}'s Cloudstorage files")
    while True:
        if cloudstorageCount >= len(cloudstorageIDList): break
        fileID, fileName = [cloudstorageIDList[cloudstorageCount], cloudstorageNameList[cloudstorageCount]]
        reqGetCloudstorageFileText = requestText(session.get(links.cloudstorageRequest.format(f"user/{accountId}/{fileID}"), headers=headers, data=""), False)
        if (bSaveEmptyCloudstorage == "false") and (not reqGetCloudstorageFileText):
            cloudstorageCount += 1
            print(f"{cloudstorageCount}: Skipping {fileName} because it's empty.")
        else:
            cloudstorageFilePath = os.path.join(userCSPath, f"{fileName}")
            with open(cloudstorageFilePath, "w", encoding = "utf-8") as fileToSave: fileToSave.write(reqGetCloudstorageFileText)
            cloudstorageCount += 1
            fileSize = roundSize(cloudstorageFilePath)
            print(f"{cloudstorageCount}: Dumped {fileName} ({fileSize} KB)")
    print(f"\n{displayName}'s Cloudstorage files have been successfully saved in {userCSPath}.\n")

# Get and dump the global Cloudstorage.
if bDumpGlobalCloudstorage == "true":
    globalCSPath = os.path.join(path, "Global Cloudstorage")
    if not os.path.exists(globalCSPath): os.makedirs(globalCSPath)
    reqGetCloudstorageText = requestText(session.get(links.cloudstorageRequest.format("system"), headers=headers, data="{}"), True)
    cloudstorageIDList, cloudstorageNameList, cloudstorageCount = [[], [], 0]
    for key in reqGetCloudstorageText:
        cloudstorageIDList.append(key['uniqueFilename'])
        cloudstorageNameList.append(key['filename'])
    print(f"Starting to dump {len(cloudstorageIDList)} global Cloudstorage files")
    while True:
        if cloudstorageCount >= len(cloudstorageIDList): break
        fileID, fileName = [cloudstorageIDList[cloudstorageCount], cloudstorageNameList[cloudstorageCount]]
        reqGetCloudstorageFileText = requestText(session.get(links.cloudstorageRequest.format(f"system/{cloudstorageIDList[cloudstorageCount]}"), headers=headers, data=""), False)
        if (bSaveEmptyCloudstorage == "false") and (not reqGetCloudstorageFileText):
            cloudstorageCount += 1
            print(f"{cloudstorageCount}: Skipping {fileName} because it's empty.")
        else:
            cloudstorageFilePath = os.path.join(globalCSPath, f"{cloudstorageNameList[cloudstorageCount]}")
            with open(cloudstorageFilePath, "w", encoding = "utf-8") as fileToSave: fileToSave.write(reqGetCloudstorageFileText)
            cloudstorageCount += 1
            fileSize = roundSize(cloudstorageFilePath)
            print(f"{cloudstorageCount}: Dumped {fileName} ({fileSize} KB)")
    print(f"\nGlobal Cloudstorage files have been successfully saved in {globalCSPath}.\n")
    
input("Press ENTER to close the program.\n")
exit()