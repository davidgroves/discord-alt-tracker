# Discord Alt Tracker

A very simple discord bot designed to make tracking alternative characateristics of a user easy.

The original use case was for World of Warcraft guilds and other organisations to know the alternative names of characters.

## User Guide

`/alt list <discord user>` to list the character names associated with a discord user. Add your own name to see yourself.

`/alt add <class> <name>` to add an alt name to your own profile.

`/alt remove <class> <name>` to remove an alt name from your profile.

`/alt search <name>` tells you what discord user is associated with an alt name.

## How to invite to a server

[Invite Link](https://discord.com/api/oauth2/authorize?client_id=1140082321152806922&permissions=0&scope=bot)

## How to run the bot yourself.

- Checkout this git repo.
- [Setup the database](docs/SETUP_DATABASE.md).
- Set environment variables, as shown in dotenv_template. You can use a .env file for testing/dev, or actual environment variables in production.
- Setup a Python 3.10+ VirtualEnv, and install the requirements in requirements.txt.
- Run bot.py from within the VirtualEnv.

## Known Issues

- No checking for multiple characters with same name on same realm.
