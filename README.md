# Youtube downloader

A simple mp3 converter discord bot using youtube-dlp with ffmpeg.

## Setup
### Operating system
I use a debian server, I don't think it matters which OS you use, as long as you can setup
a webserver that can serve static files from './static' then you should be fine.

### Webserver
You need to setup a webserver that can serve static files from './static' folder.

### Bot
```bash
# install ffmpeg, e.g. ubuntu/debian 
sudo apt install ffmpeg

# install
pip install virtualenv [--user]

# create an env
virtualenv venv
virtualenv -p /usr/local/bin/pypy venv # using the pypy distribution

# use the env
source myenv/bin/activate

# install dependencies
pip install -r requirements.txt

cd src/

# run bot
cd bot
python main.py
```
