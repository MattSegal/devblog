#!/bin/bash
set -e
export PELICAN_GA=""
export PELICAN_HOSTURL="http://localhost:8001"
export HOT_RELOAD="1"
. ./env/bin/activate
echo ">>> Building social cards"
./build_social_cards.py
echo ">>> Cleaning"
make clean
echo ">>> Publising"
make publish
watchmedo \
    auto-restart \
    --directory ./content/ \
    --directory ./theme/ \
    --recursive \
    --patterns '*.md;*.html;*.css;*.js' \
    -- \
    make publish
