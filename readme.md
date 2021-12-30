# Fortnite Response Dumper

This program allows you to dump many Fortnite responses.

---
### Changelog:
What's new in the 1.2.1 update:
- A new config option called "Save_Empty_Cloudstorage".
  - From now on, the program will not dump empty Cloudstorage files by default.
  - You can change it via this option in the config file.
- Changed the file size info to show an additional tenth of the size.
- Fixed an issue with files paths on mobile devices.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the FortniteResponseDumper.py for the first time (or after deleting the auth.json file), you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

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