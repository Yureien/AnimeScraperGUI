# Anime Scraper (GUI)
This is a GUI version of [anime-scrapers](https://github.com/jQwotos/anime-scrapers) with extra features!
It was built using Python, Django, Python Requests module, and Python BeautifulSoup4 module.

With this, you can stream or download animes from many sites, which are given in the [anime-scrapers](https://github.com/jQwotos/anime-scrapers) repository.

## Installation

Install `django`, `requests` and `bs4` via any installer of your choice like `pip`.

Pip install command (Windows users: Delete the word `sudo`. *May require administrator privileges.*) -
```
sudo pip install django requests bs4
```
Then install this with the following commands -
```
git clone <Repo URL. I hope you know what this is.>
cd AnimeScraperWebUI
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
python manage.py runserver <PORT_NAME_FROM_1024_TO_65536>
```
## Contribution

Fork, clone, make changes, push, create PR. I will accept the PR or ask you to make changes if required.

## Credits
- [FadedCoder](https://github.com/FadedCoder)
- [jQwotos](https://github.com/jQwotos)
