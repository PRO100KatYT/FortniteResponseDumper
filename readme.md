# Fortnite Response Dumper

This program allows you to dump many Fortnite responses.

---
### Features:
- Multiple account support with two login methods: refresh token and device auth.
- The program is able to dump:
  - account and global cloudstorage,
  - user profiles and other's Save the World profiles,
  - account information,
  - BR stats & inventory,
  - user friendlists,
  - catalog responses,
  - contentpages,
  - discovery tab responses,
  - keychain,
  - timeline,
  - theater (stw world).

- A config file where you can choose which responses to dump.
---
### Changelog:
What's new in the 1.4.3 update:
- Added the ability to save Battle Royale account statistics.
- Added the ability to dump the Battle Royale inventory (bars).
- Simplified the config - now contentpages, keychain, timeline and theater can be toggled under one `Dump_Single_Responses` option.
- Temporarily fixed the issue when sometimes the priceengine response cannot be saved by making the program skip it when the error occurs.
- The program now displays a more accurate file size if needed.
- Fixed some typos.
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
