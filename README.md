# Anime Scraper (GUI)
This is a GUI version of [anime-scrapers](https://github.com/jQwotos/anime-scrapers) with extra features!
It was built using Python, Django, Python Requests module, and Python BeautifulSoup4 module.

With this, you can stream or download animes from many sites, which are given in the [anime-scrapers](https://github.com/jQwotos/anime-scrapers) repository.

This is actually a web UI, in other words, a local server. So, you can open the server website on any device on the local network by installing this repo on a PC, or even remotely if you configure it that way (Instructions not included for remote setup. Just a tip: Use localtunnel). 

Remember, this is a WIP.
## Installation

Install `django`, `requests` and `bs4` via any installer of your choice like `pip`.

Pip install command (Windows users: Delete the word `sudo`. *May require administrator privileges.*) -
```
sudo pip install django requests bs4
```
Then install this with the following commands -
```
git clone --recursive https://github.com/FadedCoder/AnimeScraperGUI.git
**OR IF YOU HAVE SSH**
git clone --recursive git@github.com:FadedCoder/AnimeScraperGUI.git

cd AnimeScraperGUI
python manage.py makemigrations
python manage.py migrate
```
## Usage

**(Linux/Mac users only with admin account)** To run on port 80:
```
sudo ./run
```
**(Any OS users with or without admin account)** To run on any port of your choice -
```
python manage.py runserver <PORT_NUMBER_FROM_1024_TO_65536>
```

Then go to [localhost](http://localhost) from the PC it is installed in.
## Contribution

Fork, clone, make changes, push, create PR. I will accept the PR or ask you to make changes if required.

## Credits
- [FadedCoder](https://github.com/FadedCoder)
- [jQwotos](https://github.com/jQwotos)
