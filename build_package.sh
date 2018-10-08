#!/usr/bin/env bash

if [ "$TRAVIS_OS_NAME" = "osx" ] ; then
    bash -x build_macos_binary.sh
elif [ "$TRAVIS_OS_NAME" = "linux" ] ; then
    sudo apt -qq update
    sudo apt install -y fakeroot libczmq-dev

    bash -x build_deb_package.sh
fi
