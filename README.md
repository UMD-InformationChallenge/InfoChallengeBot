# InfoChallengeBot
Discord Registration Bot for the UMD Information Challenge

## What is the UMD Information Challenge?

The [UMD Information Challenge](https://infochallenge.ischool.umd.edu/) is a week-long event 
that gathers teams of students from across multiple academic institutions to work with 
partnering organizations to address real-world problems, provide valuable team-building 
experience, and network with industry professionals.

More information about the UMD Information Challenge can be found at its website at:
https://infochallenge.ischool.umd.edu/

## Features

The InfoChallengeBot currently provides:
- Registration support through a very basic chatbot
- Basic moderation support (message deletion)
- Team creation and deletion

## This is not a Product

This bot requires a significant amount of programming and technical know-how and is not currently 
intended as an off-the-shelf product. The authors and contributors to this project may respond to 
your questions, but use at your own risk.

## Quick Start 
To quickly get running 
1. Clone repository
2. cd into directory
3. Run `poetry install`
1. Copy the dotenv file to '.env'
1. Edit '.env' to fill in your configuration values.
5. Run `poetry run python src/bot.py`

## Docker Stack Quick Start
This starts the front end, the database, and a database admin tool on port 8080.
You must have enabled docker swarm mode. (docker swarm init)
1. Clone repo
1. cd into directory
1. Run `docker build -t infochallengebot:1.0
1. Copy dotenv file into .env and then edit the values.
1. Start the stack like this:
```
$ docker stack deploy -c <(docker-compose config) ic
```

Bot waits 20 seconds for the DB to start up, but the MariaDB container image can take longer than that for Docker to download.
Check the bot's logs for database related errors:  `docker service logs ic_discord-bot`
If you see database connection errors, wait 5 minutes, then try:
`docker service update --force ic_discord-bot`
This makes the bot restart and try to reconnect.

## To Access Documentation
Documentation is provided through mkdocs. You can start up a mkdocs server with the command `poetry run mkdocs serve` 
after completing the installation instructions.
