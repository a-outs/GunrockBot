# GUNROCK BOT
The best bot around for UC Davis Discord Servers

[**INVITE LINK**](https://discord.com/oauth2/authorize?client_id=726048467063013376&scope=bot)

## COMMANDS

### General Commands

`help`
For help

### Course and CRN Commands (`data`)

`course [course code]`
Gives you the full course name and description, including GE's fulfilled and prerequisites.

`crn [course code]`
Gives you the CRN data of a course.

### Meme Commands (`memes`)

`cheeto`
Sends a random picture of cheeto

`boomer @user`
Calls out a user for being a boomer

`dab @user`
Dabs on dem haters

`cow @user`
Tells you how much of a true Aggie they are

`bad @user`
Calls them out for being bad

`simp @user`
Rates how much of a simp they are

### Admin Only Commands (requires manage roles permission)

`setprefix [newprefix]`
use this to set the bot prefix

`mod [mod name]`
enables or disables the specified module

`listmods`
lists all mods and whether or not they are enabled or disabled

`timeout [timeout length]`
Messages sent from commands in the `data` category will self destruct after `timeout length` seconds. Input must be an integer.
Set to 0 to disable timeout.

## CHANGELOG

### GUNROCK 1.5.3

- Added cheeto command
- `crn` will now give up-to-date information on seats available whenever possible.
- Commands are now modular and can be enabled/disabled per-server.
- Added ability to set timeout for data commands.

### GUNROCK 1.4.1

- Disabled everything except course and crn data retrieval while updates are being worked on.

### GUNROCK 1.4

- Added reaction roles message functionality.
- Cogged the bot up.
- Temporarily disabled swearjar functionality.

### GUNROCK 1.3

- Added person welcoming functionality.

### GUNROCK 1.2

- Added getCRNdata command.
- Formatted most messages to be in embeds for a cleaner look.
- Increased functionality of the telltime command.

### GUNROCK 1.1

- Reduced mentions that Gunrock does to decrease spam
- Remove function for swearjar added:  you can now deduct points from a swearjar.
- Removed score restrictions for add/remove functions. You can now add/remove integer values that aren’t 1 or 5
- Allows custom prefixes for servers
- Added getcourse command, retrieves data about a specific UC Davis course given a course code
- Added editquote command, allows for editing of existing qutoes
- Changed the manual command to help
- Removed .boomer
- Demoted Peter from admin. Gunrock is admin now

### GUNROCK 1.0

- Initial bot with swearjar and quotebook features

## CREDITS

Currently worked on by Jun and Tim.  
The Gunrock mascot and course data belong to The University of California at Davis. We do not claim ownership of either.  
