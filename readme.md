# Fortnite Response Dumper

This program allows you to dump many Fortnite responses.

---
### Features:
- Multiple account support with two login methods: refresh token and device auth.
  - You can see more info about them and choose the method when adding an account.
- The program is able to dump:
  - catalog,
  - keychain,
  - contentpages,
  - timeline,
  - user profiles,
  - other's Save the World profiles,
  - user friendlists,
  - discovery,
  - account and global cloudstorage.
- A config file where you can choose which responses to dump.
---
### Changelog:
What's new in the 1.4.0 update:
- Merged the [Anyone's Save the World Profile Dumper](https://github.com/PRO100KatYT/AnyonesSTWProfileDumper) with Fortnite Response Dumper.
- When someone else's profile0 is generated the program will now give and set the banner icon to the light blue OT11 one instead of leaving it empty.
- Fixed a crash that the generated profile0 caused on some Fortnite builds because of the build failing to find Karolina's and Joel's portraits that didn't exist yet.
- Fixed a crash that the generated profile0 caused on some Fortnite builds because of the build failing to open llamas that didn't exist yet.
- Fixed a crash that the generated profile0 caused on some Fortnite builds because of the build failing to display the banner menu when some banners didn't exist yet.
- If the ```Sorry the authorization code you supplied was not found. It is possible that it was no longer valid.``` error message will pop up, the program will no longer close. It will ask you to input the code again instead.
- Added the ```Features``` section to the readme.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the FortniteResponseDumper.py for the first time (or after deleting the config.ini file) you will be asked if you want to start the config setup process or use the default config values. If you want to start the setup, type 1, if no, type 2.

- Next, you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

- After you'll press ENTER, an Epic Games website will open. From there, login if you are not already logged into your Epic account.

- Then a page should open with content similar to this:

```json
{"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
or this:
```json
{"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```

- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now you can either dump your account's responses or someone else's Save the World profile (campaign and common_public).
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/FortniteResponseDumper/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.