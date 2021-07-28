# Youtube downloader

Simple youtube downloader discord bot and web API

 address in ytmp3/bot/config.json and ytmp3/web/config.json

## Endpoints
- /play/id => serves id.mp3 downloaded and converted from /watch?v=id (must be requested from the discord bot)

## Requirements
- docker
- docker-compose

## Setup

1. Clone the repository
2. cd into the directory
3. run the following commands
```bash
cd ./ytmp3 # relative to this file!
docker-compose up
```
4. Provide bot token in ytmp3/bot/config.json
5. Change IP in ytmp3/bot/config.json and ytmp3/web/config.json
6. You can switch the IP into a domain name, it's only needed to provide a valid URL to the users after converting is complete.
