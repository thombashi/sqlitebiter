#!/usr/bin/env bash

if [ "$TOXENV" != "build" ] ; then
    tox
fi
