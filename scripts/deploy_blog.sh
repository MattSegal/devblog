set -e
. ./env/bin/activate
make clean
make publish
aws s3 cp \
    --recursive \
    --acl public-read \
    ./output \
    s3://mattsegal.dev

aws cloudfront create-invalidation \
    --distribution-id E1N8GMO4U6RJRA \
    --paths "/*"
