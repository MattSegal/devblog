#!/usr/bin/env python
import os
from pelican.plugins import jinja2content

AUTHOR = "Matthew Segal"
SITENAME = "Matt's Dev Blog"
SITEURL = ""
HOSTNAME = "Matt's Dev Blog"
HOSTURL = os.environ["PELICAN_HOSTURL"]
THEME = "./theme"

PATH = "content"
# https://github.com/pelican-plugins/jinja2content
PLUGINS = [jinja2content]


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
DEFAULT_PAGINATION = 20

IGNORE_FILES = ["*.draft.*"]

HOT_RELOAD = os.environ.get("HOT_RELOAD", False)

os.environ["PYGMENTS_NODE_COMMAND"] = 'node' 