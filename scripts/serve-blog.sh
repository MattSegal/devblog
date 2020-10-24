#!/bin/bash
set -e
pushd output
python3 -m http.server 8001
popd