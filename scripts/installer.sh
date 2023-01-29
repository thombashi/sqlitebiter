#!/usr/bin/env bash

set -eu

if [ $UID -ne 0 ]; then
    echo 'requires superuser privilege' 1>&2
    exit 13
fi

ARCH=$(dpkg --print-architecture)
VERSION_CODENAME=$(\grep -Po "(?<=VERSION_CODENAME=)[a-z]+" /etc/os-release)
DEBFILE="${VERSION_CODENAME}_${ARCH}\.deb"

ARCHIVE_URL=$(curl -sSL https://raw.githubusercontent.com/thombashi/sqlitebiter/master/scripts/latest_release_assets.list | \grep "$DEBFILE")
TEMP_DEB="$(mktemp)"

trap "\rm -f $TEMP_DEB" 0 1 2 3 15
curl -L "$ARCHIVE_URL" -o "$TEMP_DEB"
dpkg -i "$TEMP_DEB"
