# ScrubBot

ScrubBot is a general-purpose bot created for the ScrubLords Discord server.

Currently, ScrubBot has the following command sets:
1. Server event management

## Using ScrubBot
The following lays out the available commands when using ScrubBot in your Discord server.

All commands are preceded with a "$" character.

### Server Events
ScrubBot has a set of commands for creating and running gaming events on your server.

***$event create \<name> [options]***

Options:
- -g, -game:  The name of the game being played
- -m, -max: The max number of players for the event
- -t, -time: The time the event takes place

*event create* will create a new event for the server. The provided *name* will be the name of the event,
and the provided game name is what will be used to search for the appropriate cover art on IGDB.
The provided time will be parsed using [dateparser](https://pypi.org/project/dateparser/), and so it accepts
all sorts of formats, such as:
- Tomorrow at 9pm pst
- 6/2/2020 2pm
- In one hour

***$event edit \<id> [options]***

Options:
- -n, -name: The name of the event
- -g, -game:  The name of the game being played
- -m, -max: The max number of players for the event
- -t, -time: The time the event takes place

*event edit* allows you to modify the settings of an event that you host.
It shares the same options as *event create*, with the addition of the "-n" flag for changing the event name.

***$event join \<id>***

*event join* will allow you to join an existing event.

***$event leave \<id>***

*event leave* will allow you to leave an existing event you have joined.

***$event cancel \<id>***

*event cancel* will cancel an event that you are the host of.

***$event info \<id>***

*event info* will display all information on the event with the given id.

***$event start \<id>***

*event start* will immediately start an event that you are the host of, notifying all players that it is starting.

***$event players \<id>***

*event players* will display all players currently joined to the given event.

***$event active***

*event active* will display all active events in the current server. 

## Developing ScrubBot
This guide currently assumes that you're developing ScrubBot on Windows.

### Requirements
1. Python 3.7 (https://www.python.org/downloads/)
2. PostgreSQL 4.21 (https://www.postgresql.org/)
3. A Discord bot account
4. An IGDB account and API key

Using a higher version of Python is probably fine, but ideally you'd work in the same version.

### Installing Python
Running the Python installer above should handle just about everything for you.
To verify that you've got Python installed and in your PATH, run the following from anywhere on the command line:

`python --version`

If you have Python 2 installed, this might show that version.
In that case, any time this guide asks you to run something starting with `python`, use `py -3` instead.

Additionally, verify that pip is installed using the following:

`pip3 --version`

We use pip3, just in case you have Python 2 already installed.
This will just ensure that we use the Python 3 version.

### Python requirements
The repo contains a requirements.txt file for installing the necessary Python requirements.
After Python is installed, run the following from the top level of the repo folder:

`pip3 install -r requirements.txt`

### Creating a Discord bot account
You will need a Discord bot for this to run on for local work.

First, go to the [Discord Developer Dashboard](https://discord.com/developers/applications). In the top right, select "New Application", and give it a name.

![](https://i.imgur.com/GvO38c9.png)

You should now be looking at the main page for your Discord application. From here, select the "Bot" tab.
Here, select "Add Bot" to add a Bot user to this application.

![](https://i.imgur.com/o9LSelb.png)

Give your bot a name, and click to reveal your bot's token. Copy this down somewhere because we will need it later.

![](https://i.imgur.com/ceIZil3.png)

Next, we want to invite your bot to the Discord server you will be testing in.
You need to be the server owner in order to add bots, so create a new test server if necessary.

Navigate to the "OAuth2" tab of your Discord application. We are going to be generating the invite link for your bot.

In the "Scopes" box, select "bot". This will bring up another box below titled "Bot Permissions".
In that box, select the following options:
1. View Channels
2. Send Messages
3. Manage Messages
4. Embed Links
5. Attach Files
6. Read Message History
7. Mention Everyone
8. Use External Emojis
9. Add Reactions

Your selected boxes should look like this

![](https://i.imgur.com/23rTMJi.png)

Now, copy the URL marked in red, and navigate to it in your browser.
This should redirect you to a dialogue to invite the bot to servers you own.
Once the bot is in your server, you're done with the Discord stuff.

### Setting up the database
After installing and setting up PostgreSQL on your machine, you will need to create the scrubbot database.
This repo contains a file "scrubbot_db_backup". You should be able to use the pg_restore function with this file to create the necessary schema for the database.

This file assumes you've already created a new database server, and are seeing a similar screen to this in pgAdmin

![](https://i.imgur.com/bw3JM4U.png)

As you can see, I have my server with just the default postgres database in it.

From here, right click "Databases", and select Create > Database...

![](https://i.imgur.com/kGUPZNx.png)

In the form that opens, name your database whatever you want (I name mine scrubbot), and click "Save".

![](https://i.imgur.com/uZhuXvb.png)

You should see your new database next to postgres, and can now right click on it and select "Restore..."

![](https://i.imgur.com/WH69Pf4.png)

In the form that opens, set Filename as the path to "scrubbot_db_backup", either directly, or using the file select dialog.

If using the dialog, be sure to change Format to "All Files", and select the correct file in the repo

![](https://i.imgur.com/XkLLDTx.png)

Now, with the file selected, click "Restore" in the Restore dialog.

![](https://i.imgur.com/097jpsF.png)

All required database schema should now be created.

You will want to copy down your database URL, which should be in the form:

`postgresql://<psql username>:<psql password>@<psql host>:<psql port>/<psql database name>`

(None of the <> brackets are included)

### Getting an IGDB API key
The IGDB (Internet Games Database) is the source for game cover art that is used in the bot's embed messages.
In order to access their API, you'll need an API key, which can be obtained via their [website](https://www.igdb.com/api).
There, click "Get Key" and follow the instructions.

Once you have the key, copy it down, you'll need it later. 

### Setting up your environment variables
Finally, you need to create the necessary environment variables for the bot. Add a .env file to the root of the repo.
We're going to add the following key-value pairs to this file:

1. BOT_TOKEN=\<The Discord bot token you copied down\>
2. IGDB_KEY=\<Your IGDB API key\>
3. DATABASE_URL=\<Your PostgreSQL database URL\>

(None of the <> brackets are included)

### Running the bot locally
With everything set up, run the following from the command line in the repo folder:

`py -3 runbot.py`

Your bot should come online and will begin responding to commands.

## Need Help?
If you run into any issues running or developing for ScrubBot, please do not hesitate to reach out here, via email (makelacaleb@gmail.com), or via Discord (Syldarion#0001).
