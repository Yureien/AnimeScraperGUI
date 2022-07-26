# Anime Scraper (GUI)

**As of when this was last updated, the following sources work: AnimeHeaven. More sources will be added on/repaired in the future**

This is a GUI version of [anime_scrapers](https://github.com/jQwotos/anime_scrapers) with extra features!
It was built using Python, Django, Python Requests module, and Python BeautifulSoup4 module, and some other modules (all are listed in requirements.txt).

With this, you can stream or download animes from many sites, which are given in the [anime_scrapers](https://github.com/jQwotos/anime_scrapers) repository.

This is actually a web UI, in other words, a local server. So, you can open the server website on any device on the local network by installing this repo on a PC, or even remotely if you configure it that way (Instructions not included for remote setup. Just a tip: Use localtunnel).

**IMPORTANT:** *Please note that this server was made for local use personally. The security standards are low. If you wish to use it publicly/with friends who want to hack you, please configure this with a robust web server such as [Apache](https://httpd.apache.org). Also go to AnimeScraper/settings.py and set the required variables for production.*

**The downloaded videos are in `media/videos/` folder, which is automatically created.**

**NOTE: The videos are downloaded locally on host PC in the "details" page. To download it locally, press 'Download Local' in the plat page.**

Remember, this is a WIP.
## Installation

Install the modules listed in `requirements.txt` via any installer of your choice like `pip`.

Pip install command (Windows users: Delete the word `sudo`. *May require administrator privileges.*) -
```
sudo pip install -r requirements.txt
```
Then install this with the following commands -
```
git clone --recursive https://github.com/FadedCoder/AnimeScraperGUI.git
**OR IF YOU HAVE SSH**
git clone --recursive git@github.com:FadedCoder/AnimeScraperGUI.git

cd AnimeScraperGUI
python manage.py makemigrations
python manage.py makemigrations Scraper
python manage.py migrate
```
## Usage

**(Linux/Mac users only)** To run on port 8080:
```
./run
```

**RECOMMENDED - (Any OS users)** To run on any port of your choice -
```
python manage.py runserver <PORT_NUMBER_FROM_1024_TO_65536>
```

If you want to run between ports 1 to 1024, you need administrator privileges. For example, on port 80, the local url will be "http://localhost".

Then go to [localhost](http://localhost:8080) from the PC it is installed in. If you changed the port number to something other than 8080, it would be [http://localhost:PORT](http://localhost:PORT)
## Contribution

Fork, clone, make changes, push, create PR. I will accept the PR or ask you to make changes if required.

I will be very, very happy if you make a PR! :)

## Credits
- [Yureien](https://github.com/Yureien)
- [jQwotos](https://github.com/jQwotos)
