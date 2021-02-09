# GUNROCK BOT
The best bot around for UC Davis Discord Servers

## FEATURES

While we work on some updates, the only features currently enabled for the bot are course and crn data retrieval.

## COMMANDS

### General Commands

help - run this to get a list of commands

### Course and CRN Commands

(prefix)course [course code]: Gives you the full course name and description. Make sure to put in zeros! For example, to get data about DRA 001, make sure those two 0's are there.

(prefix)crn [course code]: Gives you the CRN data of a singular course. Again, make sure zeros are there.

### Admin Only Commands

rolemessagesetup - use this to set up the reaction roles message, the emojis, and their respective roles. Requires the manage guild permission  
(prefix)rolemessagesetup [reaction role message content],[emojis in their respective order, seperated by %],[role names, seperated by %]  
  
rolesetup - run this command to send the official message that users would react to to recieve their roles. Requires the manage guild permission  
(prefix)rolesetup  
  
setprefix - use this to set the bot prefix  
(prefix)setprefix [newprefix]  

## CHANGELOG

### GUNROCK 1.5

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
Thanks to Peter for hosting the bot.  
The Gunrock mascot and course data belong to The University of California at Davis. We do not claim ownership of either.  
