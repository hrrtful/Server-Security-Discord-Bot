# Server-Security-Discord-Bot
Anti-Nuke capabilities, powerful moderation features, auto punishments, captcha-verification and more.


## Installation
Install all dependencies:
* `pip install -r requirements.txt`
* Then add your Discord token, which you can find in the Discord developer portal, to the very bottom of the `main.py` file 
* This bot have to use the "server members intent", so you have to enable it in the Discord's developers portal
Finally you can host the bot and invite it to your own server.


## Features
With some powerful features, Server Security will be able to protect your server from being nuked, raided, malicous users, spammer etc.
* Anti-Nuke
* Captcha-Verification
* Join-Filter
* Auto-Moderation
* Panic-Mode
* Moderation Commands
* General Commands
* Multi guild support
Tip: The bot needs the ADMINISTRATOR permission! Restrictions do not affect members with ADMINISTRATOR permission!


## Commands
<...> Duty | [...] Optional
```
s!help
s!setup
s!features
s!settings
s!permissions
s!about
s!invite
s!serverinfo
s!userinfo [member]
s!prefix <new prefix>
s!inviteinfo <link/code>
s!commands
s!bug (This command sends a message to my server with the bug, you should maybe not change this command)
s!fetchuser <user id>
s!snipe
s!lock [#channel/id]
s!unlock [#channel/id]
s!ban <member> [reason]
s!kick <member> [reason] 
s!unban <user id>
s!mute <member> [reason]
s!unmute <member>
s!clear <amount>
s!nuke
s!role <add/remove> <member> <role>
```
For more information about a feature/module `s!feature <feature>`

## Extra
Server Security supports multi-guild functionality, which means it can run on multiple servers, with individual options for each server.
