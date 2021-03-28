#!/bin/bash

BUILD_ENV=_linux_build_env

python3 -m pip install -U virtualenv
mkdir -p $BUILD_ENV
python3 -m virtualenv $BUILD_ENV
cd "$BUILD_ENV" || exit 1

pwd
ls bin/activate

source bin/activate
