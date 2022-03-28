version = "1.3.6"
configVersion = "1.3.4"
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
    discovery = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/creative/discovery/surface/{0}"
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
        dumpOptionsJson = {"Dump_Catalog": "Catalog (Item Shop)", "Dump_Keychain": "Keychain", "Dump_Contentpages": "Contentpages (News)", "Dump_Timeline": "Timeline", "Dump_Theater": "Theater (StW World)", "Dump_Profiles": "Account Profiles", "Dump_Friendlists": "Epic Friends related responses", "Dump_Account_Cloudstorage": "Account Cloudstorage", "Dump_Global_Cloudstorage": "Global Cloudstorage", "Dump_Discovery": "Discovery Tab responses"}
        for option in dumpOptionsJson: iList.append(validInput(f"Do you want the program to dump the {dumpOptionsJson[option]}?\nValid vaules: {', '.join(boolValues)}.", boolValues))
        iDump_Catalog, iDump_Keychain, iDump_Contentpages, iDump_Timeline, iDump_Theater, iDump_Profiles, iDump_Friendlists, iDump_Account_Cloudstorage, iDump_Global_Cloudstorage, iDump_Discovery = iList
        iSave_Empty_Cloudstorage = validInput(f"Do you want the program to save Global Cloudstorage files that are empty?\nValid vaules: {', '.join(boolValues)}.", boolValues)
    else: iAuthorization_Type, iLanguage, iDump_Catalog, iDump_Keychain, iDump_Contentpages, iDump_Timeline, iDump_Theater, iDump_Profiles, iDump_Friendlists, iDump_Account_Cloudstorage, iDump_Global_Cloudstorage, iSave_Empty_Cloudstorage, iDump_Discovery = ["token", "en", "true", "true", "true", "true", "true", "true", "true", "true", "true", "false", "true"]
    with open(configPath, "w") as configFile: configFile.write(f"[Fortnite_Response_Dumper_Config]\n\n# Which authentication method do you want the program to use?\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\n# Valid vaules: token, device.\nAuthorization_Type = {iAuthorization_Type}\n\n# What language do you want some of the saved responses to be?\n# Valid vaules: de, ru, ko, en, it, fr, es, ar, ja, pl, es-419, tr.\nLanguage = {iLanguage}\n\n# Do you want the program to dump the Catalog (Item Shop)?\n# Valid vaules: true, false.\nDump_Catalog = {iDump_Catalog}\n\n# Do you want the program to dump the Keychain?\n# Valid vaules: true, false.\nDump_Keychain = {iDump_Keychain}\n\n# Do you want the program to dump the Contentpages (News)?\n# Valid vaules: true, false.\nDump_Contentpages = {iDump_Contentpages}\n\n# Do you want the program to dump the Timeline?\n# Valid vaules: true, false.\nDump_Timeline = {iDump_Timeline}\n\n# Do you want the program to dump the Theater (StW World)?\n# Valid vaules: true, false.\nDump_Theater = {iDump_Theater}\n\n# Do you want the program to dump the account profiles?\n# Valid vaules: true, false.\nDump_Profiles = {iDump_Profiles}\n\n# Do you want the program to dump the Epic Friends related responses?\n# Valid vaules: true, false.\nDump_Friendlists = {iDump_Friendlists}\n\n# Do you want the program to dump the account Cloudstorage?\n# Valid vaules: true, false.\nDump_Account_Cloudstorage = {iDump_Account_Cloudstorage}\n\n# Do you want the program to dump the global Cloudstorage?\n# Valid vaules: true, false.\nDump_Global_Cloudstorage = {iDump_Global_Cloudstorage}\n\n# Do you want the program to save Cloudstorage files that are empty?\n# Valid vaules: true, false.\nSave_Empty_Cloudstorage = {iSave_Empty_Cloudstorage}\n\n# Do you want the program to dump the Discovery Tab responses?\n# Valid vaules: true, false.\nDump_Discovery = {iDump_Discovery}\n\n# Do not change anything below.\n[Config_Version]\nVersion = FRD_{configVersion}")
    print("The config.ini file was generated successfully.\n")
try:
    config.read(configPath)
    configVer, authType, lang, bDumpCatalog, bDumpKeychain, bDumpContentpages, bDumpTimeline, bDumpTheater, bDumpProfiles, bDumpFriendlists, bDumpAccountCloudstorage, bDumpGlobalCloudstorage, bSaveEmptyCloudstorage, bDumpDiscovery = [config['Config_Version']['Version'], config['Fortnite_Response_Dumper_Config']['Authorization_Type'].lower(), config['Fortnite_Response_Dumper_Config']['Language'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Catalog'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Keychain'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Contentpages'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Timeline'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Theater'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Profiles'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Friendlists'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Account_Cloudstorage'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Global_Cloudstorage'].lower(), config['Fortnite_Response_Dumper_Config']['Save_Empty_Cloudstorage'].lower(), config['Fortnite_Response_Dumper_Config']['Dump_Discovery'].lower()]
except:
    customError("The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
checkValuesJson, trueValues = [{"Authorization_Type": {"value": authType, "validValues": ["token", "device"]}, "Language": {"value": lang, "validValues": langValues}, "Dump_Catalog": {"value": bDumpCatalog, "validValues": boolValues}, "Dump_Keychain": {"value": bDumpKeychain, "validValues": boolValues}, "Dump_Contentpages": {"value": bDumpContentpages, "validValues": boolValues}, "Dump_Timeline": {"value": bDumpTimeline, "validValues": boolValues}, "Dump_Theater": {"value": bDumpTheater, "validValues": boolValues}, "Dump_Profiles": {"value": bDumpProfiles, "validValues": boolValues}, "Dump_Friendlists": {"value": bDumpFriendlists, "validValues": boolValues}, "Dump_Account_Cloudstorage": {"value": bDumpAccountCloudstorage, "validValues": boolValues}, "Dump_Global_Cloudstorage": {"value": bDumpGlobalCloudstorage, "validValues": boolValues}, "Save_Empty_Cloudstorage": {"value": bSaveEmptyCloudstorage, "validValues": boolValues}, "Dump_Discovery": {"value": bDumpDiscovery, "validValues": boolValues}}, 0]
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

if bDumpCatalog == bDumpKeychain == bDumpContentpages == bDumpTimeline == bDumpTheater == bDumpProfiles == bDumpFriendlists == bDumpDiscovery == bDumpAccountCloudstorage == bDumpGlobalCloudstorage == "false": print(f"You set everything the program can save to false in the config. Why are we still here? Just to suffer?\n")
headers = {"User-Agent": "Fortnite/++Fortnite+Release-19.40-CL-19215531 Windows/10.0.19043.1.768.64bit", "Authorization": f"bearer {accessToken}", "Content-Type": "application/json", "X-EpicGames-Language": lang, "Accept-Language": lang}

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
    profiles = ["athena", "campaign", "collection_book_people0", "collection_book_schematics0", "collections", "common_core", "common_public", "creative", "metadata", "outpost0", "profile0", "recycle_bin", "theater0", "theater1", "theater2"] # profile0 has to be after campaign, common_core, common_public and metadata since the program is going to recreate it using them.
    print(f"Starting to dump {len(profiles)} {displayName}'s profiles")
    profileCount = 0
    for profileId in profiles:
        profileCount += 1
        profileFilePath, bProfileDumped = [os.path.join(profilePath, f"{profileId}.json"), False]
        if profileId == "profile0":
            campaignPath, commonCorePath, commonPublicPath, metadataPath = [os.path.join(profilePath, f"campaign.json"), os.path.join(profilePath, f"common_core.json"), os.path.join(profilePath, f"common_public.json"), os.path.join(profilePath, f"metadata.json")]
            if (os.path.exists(campaignPath) and os.path.exists(commonCorePath) and os.path.exists(commonPublicPath) and os.path.exists(metadataPath)):
                with open(campaignPath, "r") as getCampaign, open(commonCorePath, "r") as getCommonCore, open(commonPublicPath, "r") as getCommonPublic, open(metadataPath, "r") as getMetadata: campaign, common_core, common_public, metadata_ = [json.loads(getCampaign.read()), json.loads(getCommonCore.read()), json.loads(getCommonPublic.read()), json.loads(getMetadata.read())]
                for item in campaign['items']:
                    if campaign['items'][f'{item}']['templateId'].lower().startswith("worker:"): campaign['items'][f'{item}']['attributes']['portrait'] = f"/Game/UI/Icons/Icon-Worker/IconDefinitions/{campaign['items'][f'{item}']['attributes']['portrait'].split(':')[-1]}.{campaign['items'][f'{item}']['attributes']['portrait'].split(':')[-1]}"
                profile0 = {"_id":"","created":"","updated":"","rvn":0,"wipeNumber":1,"accountId":"","profileId":"profile0","version":"","items":{},"stats":{"templateId":"profile_v2","attributes":{"node_costs":{},"mission_alert_redemption_record":{},"twitch":{},"client_settings":{},"level":1,"named_counters":{},"default_hero_squad_id":"","collection_book":{"pages":["CollectionBookPage:pageheroes_ninja","CollectionBookPage:pageheroes_outlander","CollectionBookPage:pageheroes_commando","CollectionBookPage:pageheroes_constructor","CollectionBookPage:pagepeople_defenders","CollectionBookPage:pagepeople_leads","CollectionBookPage:pagepeople_uniqueleads","CollectionBookPage:pagepeople_survivors","CollectionBookPage:pageranged_assault_weapons","CollectionBookPage:pageranged_shotgun_weapons","CollectionBookPage:page_ranged_pistols_weapons","CollectionBookPage:pageranged_snipers_weapons","CollectionBookPage:pageranged_shotgun_weapons_crystal","CollectionBookPage:pageranged_assault_weapons_crystal","CollectionBookPage:page_ranged_pistols_weapons_crystal","CollectionBookPage:pageranged_snipers_weapons_crystal","CollectionBookPage:pagetraps_wall","CollectionBookPage:pagetraps_ceiling","CollectionBookPage:pagetraps_floor","CollectionBookPage:pagemelee_swords_weapons","CollectionBookPage:pagemelee_swords_weapons_crystal","CollectionBookPage:pagemelee_axes_weapons","CollectionBookPage:pagemelee_axes_weapons_crystal","CollectionBookPage:pagemelee_scythes_weapons","CollectionBookPage:pagemelee_scythes_weapons_crystal","CollectionBookPage:pagemelee_clubs_weapons","CollectionBookPage:pagemelee_clubs_weapons_crystal","CollectionBookPage:pagemelee_spears_weapons","CollectionBookPage:pagemelee_spears_weapons_crystal","CollectionBookPage:pagemelee_tools_weapons","CollectionBookPage:pagemelee_tools_weapons_crystal","CollectionBookPage:pageranged_explosive_weapons"]},"quest_manager":{},"bans":{},"gameplay_stats":[],"inventory_limit_bonus":0,"current_mtx_platform":"Epic","weekly_purchases":{},"daily_purchases":{},"mode_loadouts":[],"in_app_purchases":{},"daily_rewards":{},"monthly_purchases":{},"xp":0,"homebase":{"townName":"","bannerIconId":"","bannerColorId":"","flagPattern":-1,"flagColor":-1},"packs_granted":0}},"commandRevision":0} # profile0 template from Lawinserver
                profile0['_id'], profile0['created'], profile0['updated'], profile0['rvn'], profile0['wipeNumber'], profile0['accountId'], profile0['version'], profile0['items'], profile0['commandRevision'] = [campaign['_id'], campaign['created'], campaign['updated'], campaign['rvn'], campaign['wipeNumber'], campaign['accountId'], campaign['version'], {**campaign['items'], **common_core['items'], **metadata_['items']}, campaign['commandRevision']]
                campaignAttrs, commonCoreAttrs, commonPublicAttrs = [{"node_costs": "node_costs", "mission_alert_redemption_record": "mission_alert_redemption_record", "twitch": "twitch", "client_settings": "client_settings", "level": "level", "quest_manager": "quest_manager", "gameplay_stats": "gameplay_stats", "inventory_limit_bonus": "inventory_limit_bonus", "mode_loadouts": "mode_loadouts", "daily_rewards": "daily_rewards", "xp": "xp", "packs_granted": "packs_granted"}, {"bans": "ban_history", "current_mtx_platform": "current_mtx_platform", "weekly_purchases": "weekly_purchases", "daily_purchases": "daily_purchases", "in_app_purchases": "in_app_purchases"}, {"townName": "homebase_name", "bannerIconId": "banner_icon", "bannerColorId": "banner_color"}]
                for attr in campaignAttrs:
                    try: profile0['stats']['attributes'][f'{attr}'] = campaign['stats']['attributes'][f'{campaignAttrs[f"{attr}"]}']
                    except: []
                try: profile0['stats']['attributes']['collection_book']['maxBookXpLevelAchieved'] = campaign['stats']['attributes']['collection_book']['maxBookXpLevelAchieved']
                except: []
                for attr in commonCoreAttrs:
                    try: profile0['stats']['attributes'][f'{attr}'] = common_core['stats']['attributes'][f'{commonCoreAttrs[f"{attr}"]}']
                    except: []
                for attr in commonPublicAttrs:
                    try: profile0['stats']['attributes']['homebase'][f'{attr}'] = common_public['stats']['attributes'][f'{commonPublicAttrs[f"{attr}"]}']
                    except: []
                profile0Nodes = ['1_main_ba01a2361', '1_main_38e8a5bf4', '1_main_ad1499e010', '1_main_27c02fc60', '1_main_0011ccd10', '1_main_904080840', '1_main_609c8a9a8', '1_main_9fdb916e6', '1_main_3ffc8e9d7', '1_main_8d2c3c4d0', '1_main_fabc7c290', '1_main_b1aef23d10', '1_main_498ab88f0', '1_main_e05f04d75', '1_main_849930d55', '1_main_b1a3a3771', '1_main_77f7b7826', '1_main_0336ac827', '1_main_0abacb4e2', '1_main_702f364c0', '1_main_243215d30', '1_main_0cbf7fec0', '1_main_38ead7850', '1_main_bd2b45b61', '1_main_a16a56111', '1_main_7a5e40920', '1_main_195c3ef52', '1_main_92e3e2179', '1_main_254cfa5515', '1_main_c06961e711', '1_main_266068670', '1_main_59607c6f0', '1_main_2546ecfc0', '1_main_a7e71bed0', '1_research_0b612c970', '1_research_a157c8e30', '1_research_a4f269d10', '1_research_248fc3870', '1_research_3e28bb331', '1_research_d2ce27910', '1_research_8707af440', '1_research_c3d05c4b2', '1_research_1bc2be641', '1_research_6114fc651', '1_research_ad50db9e1', '1_research_b543610a1', '1_research_eecd426c1', '1_research_700f196a3', '1_research_a8db35494', '1_research_11c82b1d0', '1_research_f01d00360', '1_research_b5b8eb7c0', '1_research_e9f394960', '1_research_43a8f68c0', '1_research_7382d2480', '1_research_b0d9537a1', '1_research_a5cf39400', '1_research_5201143f2', '1_research_369e5eac1', '1_research_790bdd533', '1_research_307838811', '1_research_2d0f29ab1', '1_research_1538ca901', '1_research_ed5b34d91', '1_research_04b2a68a4', '1_main_b4f394680', '1_main_3e84c12d0', '1_main_0d681a741', '1_main_e9c41e050', '1_main_88f02d792', '1_main_fd10816b3', '1_main_dcb242b70', '1_main_d0b070910', '1_main_bf8f555f0', '1_main_2e3589b80', '1_main_8991222d1', '1_main_911d30562', '1_main_d1c9e5993', '1_main_826346530', '1_main_f681ab1f0', '1_main_1637f10c4', '1_main_2996f5c10', '1_main_58591e630', '1_main_8a41e9920', '1_main_0828407d3', '1_main_566bfea11', '1_main_f1eb76072', '1_main_448295574', '1_main_ff2595300', '1_main_1b6486fc0', '1_main_4bdcb2465', '1_main_986b7d201', '1_main_ad1d66991', '1_main_f6fa8ecb3', '1_main_8b125d0f0', '1_main_d4ed4a3c4', '1_main_faee79b10', '1_main_5faa4c765', '1_main_82efddb312', '1_main_2051efb31', '1_main_6e6f74400', '1_main_7064c2440', '1_main_4658a42d3', '1_main_20d6fb134', '1_main_640195112', '2_main_a3a5da870', '2_main_fb4378a61', '2_main_25efb8c70', '2_main_b8e0a6a91', '2_main_41217f7d2', '2_main_fe2869370', '2_main_19a17bde3', '2_main_d20a597a4', '2_main_6bede9b65', '2_main_a0995fcb0', '2_main_2367c82f1', '2_main_b8a9e7cc2', '2_main_f782a9cf3', '2_main_baaa5fa10', '2_main_dfa624051', '2_main_b99a48be2', '2_main_9bbf38680', '2_main_26f4fb891', '2_main_4c95a7d12', '2_main_f4e138243', '2_main_88d0c6de0', '2_main_b75effc64', '2_main_221229060', '2_main_fa6884911', '2_main_aeeef5183', '2_main_180921fb0', '2_main_63f751711', '2_main_6a6764682', '2_main_aebc27e24', '2_main_079edd2c0', '2_main_9d7fa9270', '2_main_bf1ae4c87', '2_main_75f1308c1', '2_main_a454a2615', '2_main_636f167a0', '2_main_21ce15e51', '2_main_3d00cb840', '2_main_fc5809c05', '2_main_d52b4f3e0', '2_main_be95ebe17', '2_main_2006052b6', '2_main_e1d78b190', '2_main_a9644ddd1', '2_main_117540212', '2_main_ec26c41d0', '2_main_3c068cfb0', '2_main_4e74e6f91', '2_main_b2e063fc1', '2_main_d192eec22', '2_main_d2fb71b12', '2_main_9fc3978c3', '2_main_cf6fd83e3', '2_main_5b37c9358', '2_main_f70ba14a0', '2_main_d26651800', '2_main_4c8171671', '2_main_74699c1b1', '2_main_01f9d82a0', '2_main_4d442c140', '2_main_07d55d6a0', '2_main_2d6993922', '2_main_e321e3463', '2_main_5346207c0', '2_main_04d5c4430', '2_main_a50295643', '2_main_b2a944ec4', '2_main_d80ba2e80', '2_main_ba14281e0', '2_main_07e641121', '2_main_fa6f27881', '2_main_bf56c52e2', '2_main_1fdf39db5', '2_main_93d6486a6', '2_main_166c29dc2', '2_main_a84a13c07', '2_main_cf49a9c40', '2_main_a225639b4', '2_main_d289c7c75', '2_main_f625d4f20', '2_main_2a17d7306', '2_main_e0e4352b0', '2_main_9670df2a7', '2_main_fbc34aa68', '2_main_f657b25c9', '2_main_c4bbdff80', '2_main_a1487c230', '2_main_69a5836f0', '2_main_cc1a24d76', '2_main_b98656430', '2_main_cbbb2ff11', '2_main_134007c27', '2_main_d76888e98', '2_main_9fe51adf0', '2_main_71b7c8aa0', '2_main_9fd8cee49', '2_main_ac3b8ce810', '2_main_c677c3af0', '2_main_9d4c8cd511', '2_main_1f8f85ae0', '2_main_d8d12ecf8', '3_main_3f0e7b000', '3_main_d111a2ee0', '3_main_a4c742e90', '3_main_dc39d9a60', '3_main_5147bfc91', '3_main_642745262', '3_main_1d1190e83', '3_main_223db7781', '3_main_bb28968a1', '3_main_22db38500', '3_main_924e29d91', '3_main_70c759670', '3_main_05ee62252', '3_main_68db04ee0', '3_main_5203ac5a1', '3_main_78cb0b021', '3_main_7b6ad6772', '3_main_f9620a490', '3_main_12deae460', '3_main_cdd911fa1', '3_main_3a06bc390', '3_main_e591a24b0', '3_main_e3c7c83c1', '3_main_b98f78c61', '3_main_9341def82', '3_main_54016f663', '3_main_bb09d9260', '3_main_d259fe9e0', '3_main_4363b46c1', '3_main_3dcec5d44', '3_main_211972050', '3_main_51fbb5b30', '3_main_1d3614b63', '3_main_5973f0934', '3_main_cc393d8c0', '3_main_93b01cc71', '3_main_1650b98b5', '3_main_a2eb05de0', '3_main_931cdf301', '3_main_0f646e3e2', '3_main_7cd55e053', '3_main_0cea80c20', '3_main_ad53df901', '3_main_c0c07fd02', '3_main_bbe9c2383', '3_main_41c374291', '3_main_5272ebf85', '3_main_3ea832246', '3_main_38ade9320', '3_main_62511cb01', '3_main_392b5c050', '3_main_ae0417420', '3_main_5f1ff8f01', '3_main_b22284a80', '3_main_fdea96100', '3_main_67dad5fe1', '3_main_3e101b6a5', '3_main_e5013a630', '3_main_114d8ad91', '3_main_2e9e28772', '3_main_8aec0c687', '3_main_21baebb70', '3_main_16213c9d1', '3_main_7aae50f90', '3_main_a9fee26b3', '3_main_d9b9c4a80', '3_main_da33a8740', '3_main_aaf369514', '3_main_b3ec767e5', '3_main_95a061850', '3_main_a9cd47110', '3_main_f6bcc2ac0', '3_main_5bbdca774', '3_main_4bb06ac83', '3_main_8a85e0460', '3_main_b2f8126f4', '3_main_aa2bd6745', '3_main_d17065500', '3_main_47fdebf30', '3_main_0f7cdf126', '3_main_c55707977', '3_main_9cff8acb8', '3_main_a9bdf1c40', '3_main_94beade00', '3_main_81657c2a0', '3_main_ff1800780', '3_main_4eca66830', '3_main_aa546fd04', '3_main_f6b1c09c1', '3_main_fa382d2a2', '3_main_0830e2535', '3_main_b31485f76', '3_main_4900856e7', '3_main_ba0f64d00', '3_main_b9e79e910', '3_main_844582e68', '3_main_c583b74e0', '3_main_df62b4190', '3_main_8c8c10de9', '3_main_c1c21e346', '4_main_223600910', '4_main_8014d8830', '4_main_234e42f51', '4_main_2fb647a80', '4_main_bd23d0af0', '4_main_c76c04c11', '4_main_631dbfa62', '4_main_a1cfb4ab3', '4_main_294c621c1', '4_main_e410950a2', '4_main_b2b288db0', '4_main_a30e056a0', '4_main_fca70a2b1', '4_main_eecd0c941', '4_main_f8a251ae2', '4_main_476e9f060', '4_main_8d4f9bed1', '4_main_477eabf92', '4_main_08545f6c0', '4_main_a23e778a0', '4_main_3d8125fa3', '4_main_70213e0d4', '4_main_9afb1fd60', '4_main_2a05ce670', '4_main_0b169c105', '4_main_08666d8d6', '4_main_888a664c0', '4_main_e6f4b67e0', '4_main_6e14c9711', '4_main_11d1bb631', '4_main_751262f92', '4_main_5968fe123', '4_main_6dac1dfd4', '4_main_9b36b5171', '4_main_8b174c410', '4_main_2210edd55', '4_main_96c918a20', '4_main_5406b8760', '4_main_9f152d8c6', '4_main_20f255b61', '4_main_384f84f57', '4_main_362079e30', '4_main_111c734d0', '4_main_22983e241', '4_main_cd327eaa1', '4_main_62bcc9a02', '4_main_b854d25d2', '4_main_d94772630', '4_main_d1da41ab0', '4_main_49df3cfd1', '4_main_65b1bcf51', '4_main_72793bd96', '4_main_94a92d3e7', '4_main_7cd9fda30', '4_main_908dd2be0', '4_main_155a29ba1', '4_main_1fc4328c1', '4_main_13f4802b0', '4_main_a29f04970', '4_main_ffa3b8d60', '4_main_c8a839111', '4_main_bc0e6f120', '4_main_fb88fbd52', '4_main_65a3a1de2', '4_main_0c7672723', '4_main_02652ede4', '4_main_44036cc70', '4_main_6572170a0', '4_main_ced279315', '4_main_152db9c30', '4_main_64cedc561', '4_main_ee2bc2321', '4_main_be19d3d22', '4_main_4b1d51060', '4_main_0a5d56161', '4_main_dc7e2b381', '4_main_4eed13ae1', '4_main_170f375f1', '4_main_140b284c0', '4_main_6ce978810', '4_main_6c92b3622', '4_main_fe1404bf2', '4_main_33a623670', '4_main_2c576f893', '4_main_9d72e3e50', '4_main_a1a4f7617', '4_main_da1126e08', '4_main_03bc55d00', '4_main_6ad9a53a0', '4_main_d9295a610', '4_main_a07ccefa0', '4_main_7003c8704', '4_main_c1e85d7b4', '4_main_66adedf16', '4_main_146871b30', '4_main_f0f851670', '4_main_c6ae84eb0', '4_main_2270189f0', '4_main_5da04f861', '4_main_7c7f5f5b1', '4_main_95489ef50', '1_research_7c7638680', '2_research_ea43fdb41', '2_research_45306c490', '2_research_794309e80', '2_research_8d3a925a1', '2_research_de7035662', '2_research_bc4833ee0', '2_research_cdc67fa60', '2_research_c90f99e71', '2_research_ec48272d2', '2_research_eb75bbd01', '2_research_49280c800', '2_research_ba7b225b0', '2_research_5f21793e0', '2_research_861d8ee12', '2_research_4384865e3', '2_research_69d354ca3', '2_research_e31381504', '2_research_f583eed84', '2_research_676ea9075', '2_research_ee4d092f5', '2_research_e29cc2d33', '2_research_8c57445f1', '2_research_1986ce6e1', '2_research_dc6f1ee52', '2_research_371f90623', '2_research_816377af1', '2_research_04f33fdd2', '2_research_c4dcb3993', '2_research_acf00fd11', '2_research_d71cc3522', '2_research_15f1dc0b3', '2_research_6c56aea04', '2_research_00e5b7763', '2_research_11fc257c5', '2_research_6c377c7b6', '2_research_941abaac5', '2_research_a0af3e194', '2_research_3afd81ba3', '2_research_5fb50d871', '2_research_b3f93c620', '2_research_5d47fe190', '2_research_f8bdeebb0', '2_research_c682fdd51', '2_research_81c6b0432', '2_research_d74cab422', '2_research_163260621', '2_research_72f6c6de0', '2_research_eb4af8030', '3_research_66ad113a1', '3_research_fe0bc1210', '3_research_aa1da8210', '3_research_a39241861', '3_research_bf9440313', '3_research_b43852611', '3_research_2a7f438c2', '3_research_e8cb49191', '3_research_aeb9b0780', '3_research_296889ea0', '3_research_c82820e21', '3_research_5d0cb6cf0', '3_research_87634d530', '3_research_9dac24cc1', '3_research_9a55874d0', '3_research_a1e8d6a12', '3_research_62e106c43', '3_research_f48de6842', '3_research_3a1909ab4', '3_research_cb48078a1', '3_research_6f0ef6ca5', '3_research_57056e764', '3_research_9b20cc2a3', '3_research_a7d38aea4', '3_research_8bccb9037', '3_research_4ed9f84a6', '3_research_202d50112', '3_research_0095dc2c3', '3_research_ba83ca3a3', '3_research_60b83c472', '3_research_cebb3b219', '3_research_ec3512538', '3_research_db4c9cf95', '3_research_9dbef7d52', '3_research_72a6a9015', '3_research_a78dd3873', '3_research_4877e8553', '3_research_e920b5567', '3_research_0ac5ccfd6', '3_research_97ee240b1', '3_research_4898c79d3', '3_research_ddcaa1041', '3_research_a3701b970', '3_research_ef9604c70', '3_research_868b67a00', '3_research_2e0654db1', '3_research_3bba74012', '3_research_244e0bae1', '3_research_e63953bc2', '3_research_cf78a5f20', '3_research_2989e24e1', '3_research_99d650340', '3_research_877423d00', '3_research_9b544a970', '3_research_e558c1f41', '3_research_cf908a9f2', '3_research_86c896df3', '3_research_24cde2f34', '3_research_40dca0bc1', '3_research_88ddafb05', '3_research_b708b4253', '3_research_af4dc7fb4', '3_research_c60271af5', '3_research_beb49e403', '3_research_2066c9ce7', '3_research_e1a249502', '3_research_1ef0f9b86', '3_research_18366f893', '3_research_0356c8b05', '3_research_8e5bf50b8', '3_research_a2c489547', '3_research_6ef8fb684', '3_research_330e09826', '3_research_f49975212', '3_research_eb7b4e453', '3_research_d3cc6c383', '3_research_9cde36052', '3_research_fccd6f5f9', '4_research_5d5da3875', '4_research_3465fe4c4', '4_research_0da1313b4', '4_research_f6fa2a943', '4_research_2c5e6ca32', '4_research_05f0e3251', '4_research_4ed905580', '4_research_806a452a0', '4_research_990fa7030', '4_research_fd6399601', '4_research_bede637c1', '4_research_6085ab582', '4_research_1782f61f2', '4_research_87bc668a3', '4_research_7c66e51a3', '4_research_0af63dbb1', '4_research_7a19bc553', '4_research_d8df26f42', '4_research_df4c1eb61', '4_research_1f3130d74', '4_research_24ecb6ed0', '4_research_6970ca911', '4_research_6950520a0', '4_research_0002ffce0', '4_research_ade43eb42', '4_research_cf5201c53', '4_research_a442e02e5', '4_research_c498d7916', '4_research_949685757', '4_research_5b2432e08', '4_research_c03156729', '4_research_86ea19cb10', '4_research_8a5cb4bd4', '4_research_2ac5dffe2', '4_research_96fcf31f4', '4_research_62f4d4c75', '4_research_e4f5b7d33', '4_research_6e74626d6', '4_research_ee28e1455', '4_research_d9b9acc97', '4_research_85834f016', '4_research_2d3408466', '4_research_d39889354', '4_research_cb52ed2e6', '4_research_b794a99c7', '4_research_e68b273f8', '4_research_e122d94b8', '4_research_92602bb17', '4_research_d59f481a7', '4_research_08e6699f8', '4_research_57f9b1498', '4_research_866e34969', '4_research_fbc54b5110', '4_research_c2263dd311', '4_research_85880b7a9', '4_research_29ab3fad9', '4_research_c510196d5', '4_research_77b7b7e021', '4_research_fbd13e0b20', '4_research_8c4ff2ff9', '4_research_9041558119', '4_research_50ad3c3a18', '4_research_bd65896217', '4_research_6de82be116', '4_research_1a3360f815', '4_research_5b05f0cd14', '4_research_143d055a13', '4_research_4b2b314212', '4_research_60becf5c11', '4_research_ffbeb25a5', '4_research_9f67db025', '4_research_dcf7d2104', '4_research_d469f49d4', '4_research_0b4e2eb53', '4_research_b0cbc67f2', '4_research_297cf12b1', '4_research_d178232f0', '4_research_143a1b010', '4_research_4cb258320', '4_research_4d72e54c1', '4_research_6d8f7dab2', '4_research_800c36e52', '4_research_7de649371', '4_research_6c012b1e3', '4_research_66a77bd23', '4_research_42b6496f1', '4_research_f1d475263', '4_research_a901dffe2', '4_research_37206d211', '4_research_478935174', '4_research_fd9a30f10', '4_research_b01ae71c0', '4_research_8c0d8b320', '4_research_5d2134621', '4_research_7c9260f62', '4_research_424af64a3', '4_research_7addbb805', '4_research_fbbd71c96', '4_research_30c626c17', '4_research_6421fcaf8', '4_research_e5101a759', '4_research_41ed22ce10', '4_research_4c1080774', '4_research_108dcec92', '4_research_f31044d14', '4_research_c858e35a5', '4_research_468e857a6', '4_research_0bee01b35', '4_research_040079b07', '4_research_1acfc7918', '4_research_8ebf80409', '4_research_303e53cc10', '4_research_bde783f111', '4_research_36cf54759', '4_research_e4ca598f8', '4_research_34b078c57', '4_research_ea348b7e6', '4_research_4857ffc06', '4_research_8006526c4', '4_research_9509cdbc7', '4_research_ced5c91e8', '4_research_7a4057e95', '4_research_e5b708ac9', '4_research_a22c720c9', '4_research_b406b19221', '4_research_93fb640920', '4_research_c6ac6dcd19', '4_research_bd62253618', '4_research_4f0bf50f17', '4_research_e5f6b93d8', '4_research_51ba89697', '4_research_7be60d1f6', '4_research_e05201f55', '4_research_67582b143', '4_research_ec61c87b11', '4_research_a10a422f12', '4_research_f956124d13', '4_research_4e145e6814', '4_research_0e591ba215', '4_research_822b8ca716', 'rtrunk_1_0', 'rtrunk_1_1', 'rtrunk_2_0', 'rtrunk_2_1', 'rtrunk_3_0', 'rtrunk_3_1', 'rtrunk_4_0']
                for node in profile0Nodes: profile0['items'][f'HomebaseNode:t{node}'] = {"templateId": f'HomebaseNode:t{node}', "attributes": {"item_seen": True}, "quantity": 1}
                with open(profileFilePath, "w") as fileToSave: json.dump(profile0, fileToSave, indent = 2)
                bProfileDumped = True
            else: print(f"{profileCount}: Failed to recreate and dump the {profileId} profile")
        else:
            reqGetProfileText = requestText(session.post(links.profileRequest.format(accountId, profileId), headers=headers, data="{}"), True)
            with open(profileFilePath, "w") as fileToSave: json.dump(reqGetProfileText['profileChanges'][0]['profile'], fileToSave, indent = 2)
            bProfileDumped = True
        fileSize = roundSize(profileFilePath)
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
        print(f"Dumped the {friendslist[1]} ({fileSize} KB)")
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

# Get and dump the Discovery responses.
if bDumpDiscovery == "true":
    discoveryPath, testCohorts = [os.path.join(path, f"{displayName}'s Discovery Tab"), []]
    if not os.path.exists(discoveryPath): os.makedirs(discoveryPath)
    reqGetDiscoveryFrontend = requestText(session.post(links.discovery.format(accountId), headers=headers, json={"surfaceName":"CreativeDiscoverySurface_Frontend","revision":-1,"partyMemberIds":[accountId],"matchmakingRegion":"EU"}), True)
    discoveryFrontendFilePath = os.path.join(discoveryPath, "discovery_frontend.json")
    with open(discoveryFrontendFilePath, "w", encoding = "utf-8") as fileToSave: json.dump(reqGetDiscoveryFrontend, fileToSave, indent = 2, ensure_ascii = False)
    fileSize = roundSize(discoveryFrontendFilePath)
    print(f"Dumped Discovery - Frontend ({fileSize} KB)")
    try: testCohorts = reqGetDiscoveryFrontend['TestCohorts'] # the TestCohorts have to be grabbed from the "Discovery - Surface Frontend" response
    except: []
    if testCohorts:
        for panelName in reqGetDiscoveryFrontend['Panels']:
            panelName, pageIndex = [panelName['PanelName'], 0]
            while True:
                pageIndex += 1
                reqGetPanel = requestText(session.post(links.discovery.format(f'page/{accountId}'), headers=headers, json={"surfaceName":"CreativeDiscoverySurface_Frontend","panelName":panelName,"pageIndex":pageIndex,"revision":-1,"testCohorts":testCohorts,"partyMemberIds":[accountId],"matchmakingRegion":"EU"}), True)
                pageWord = f" (Page {pageIndex})"
                if ((reqGetPanel['hasMore'] == False) and (pageIndex == 1)): panelFilePath, pageWord = [os.path.join(discoveryPath, f"discovery_{panelName.replace(' ', '')}.json".lower()), ""]
                else:
                    panelFilePath = os.path.join(discoveryPath, panelName)
                    if not os.path.exists(panelFilePath): os.makedirs(panelFilePath)
                    panelFilePath = os.path.join(panelFilePath, f"discovery_{panelName.replace(' ', '')}{pageIndex}.json".lower())
                with open(panelFilePath, "w", encoding = "utf-8") as fileToSave: json.dump(reqGetPanel, fileToSave, indent = 2, ensure_ascii = False)
                fileSize = roundSize(panelFilePath)
                print(f"Dumped Discovery - {panelName}{pageWord} ({fileSize} KB)")
                if reqGetPanel['hasMore'] == False: break
    reqGetDiscoveryLibrary = requestText(session.post(links.discovery.format(accountId), headers=headers, json={"surfaceName":"CreativeDiscoverySurface_Library","revision":-1,"partyMemberIds":[accountId],"matchmakingRegion":"EU"}), True)
    discoveryLibraryFilePath = os.path.join(discoveryPath, "discovery_library.json")
    with open(discoveryLibraryFilePath, "w", encoding = "utf-8") as fileToSave: json.dump(reqGetDiscoveryLibrary, fileToSave, indent = 2, ensure_ascii = False)
    fileSize = roundSize(discoveryLibraryFilePath)
    print(f"Dumped Discovery - Library ({fileSize} KB)\n\n{displayName}'s Discovery Tab responses have been successfully saved in {discoveryPath}.\n")
    
input("Press ENTER to close the program.\n")
exit()