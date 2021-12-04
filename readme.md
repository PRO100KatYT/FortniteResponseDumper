# Fortnite Profile Dumper

This program allows you to dump your Fortnite account profiles.

---
### Changelog:
What's new in the 1.1.0 update:
- The program is now able to automatically open webpages for the auth code.
- Added another link to get the auth token if you're already logged in your browser.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the FortniteProfileDumper.py, you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

- After you'll press ENTER, an Epic Games website will open. From there, login if you are not already logged into your Epic account.

- Then a page should open with content similar to this:

```json
{"redirectUrl":"https://accounts.epicgames.com/fnauth?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has logged in. Now the profiles will be dumped.

- Congratulations, you just dumped your Fortnite account profiles!