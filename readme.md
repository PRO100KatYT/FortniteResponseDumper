# Fortnite Response Dumper

This program allows you to dump many Fortnite responses.

---
### Changelog:
What's new in the 1.3.3 update:
- The program is now able to dump the profile0 profile.
  - Since this profile is no longer obtainable from Epic servers, the program recreates it using the profiles it was split to (campaign, common_core, common_public and metadata) plus adds maxed out Skill Tree and Research nodes in order to give the profile more functionality. I might add more improvements into it in the future.
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

- Now the program will start to dump the responses.

- Congratulations, you just dumped Fortnite responses!

---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/FortniteResponseDumper/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.

---