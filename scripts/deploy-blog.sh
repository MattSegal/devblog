#!/bin/bash
set -e
. ./env/bin/activate
export PELICAN_GA="UA-103174696-6"
export PELICAN_HOSTURL="https://mattsegal.dev"
echo ">>> Building social cards"
./build_social_cards.py
echo ">>> Cleaning"
make clean
echo ">>> Publising"
make publish
echo ">>> Deploying"
aws s3 cp \
    --recursive \
    --acl public-read \
    ./output \
    s3://mattsegal.dev
