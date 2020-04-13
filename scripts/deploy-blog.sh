set -e
. ./env/bin/activate
export PELICAN_GA="UA-103174696-6"
export PELICAN_HOSTURL="https://mattsegal.dev"
make clean
make publish
aws s3 cp \
    --recursive \
    --acl public-read \
    ./output \
    s3://mattsegal.dev
