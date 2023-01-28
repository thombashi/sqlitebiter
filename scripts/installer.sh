#!/usr/bin/env bash

set -eu

if [ $UID -ne 0 ]; then
    echo 'requires superuser privilege' 1>&2
    exit 13
fi

ARCH=$(dpkg --print-architecture)
CODENAME=$(lsb_release -c | awk '{print $2}')
DEBFILE=$CODENAME\_$ARCH\.deb

ARCHIVE_URL=$(curl -sSL https://api.github.com/repos/thombashi/sqlitebiter/releases/latest | jq -r '.assets[].browser_download_url' | \grep $DEBFILE)
TEMP_DEB="$(mktemp)"

trap "\rm -f $TEMP_DEB" 0 1 2 3 15
curl -L "$ARCHIVE_URL" -o "$TEMP_DEB"
dpkg -i "$TEMP_DEB"
