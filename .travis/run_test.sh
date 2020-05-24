#!/usr/bin/env bash

if [ "$TOXENV" != "build" ] ; then
    tox -- --md-report-color never --md-report-zeros empty
fi
