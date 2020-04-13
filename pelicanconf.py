#!/usr/bin/env python
import os

AUTHOR = "Matthew Segal"
SITENAME = "Matt Segal Dev"
SITEURL = ""
HOSTNAME = "Matt Segal Dev"
HOSTURL = os.environ["PELICAN_HOSTURL"]
THEME = "./theme"

PATH = "content"


TIMEZONE = "Australia/Melbourne"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = []
SOCIAL = []
DEFAULT_PAGINATION = 10
