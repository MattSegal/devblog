set -e
export PELICAN_GA=""
export PELICAN_HOSTURL="file:///home/matt/code/devblog/output"
. ./env/bin/activate
make clean
make publish
