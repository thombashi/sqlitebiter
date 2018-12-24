#!/usr/bin/env bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
    if ! type python3 > /dev/null 2>&1; then
        # Install Python3 on osx
        brew upgrade python
    fi

    pip3 install setuptools tox --upgrade
else
    pip install setuptools --upgrade

    if [ "$TOXENV" != "build" ] ; then
        pip install tox --upgrade
    fi
fi
