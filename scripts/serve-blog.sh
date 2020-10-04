#!/bin/bash
set -e
pushd output
python3 -m http.server
popd