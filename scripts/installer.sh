#!/usr/bin/env bash

set -eu

if [ $UID -ne 0 ]; then
    echo 'requires superuser privilege' 1>&2
    exit 13
fi

ARCH=$(dpkg --print-architecture)
VERSION_CODENAME=$(\grep -Po "(?<=VERSION_CODENAME=)[a-z]+" /etc/os-release)

CACHE_DIR_PATH="/var/cache/sqlitebiter"
RELEASE_ASSETS="${CACHE_DIR_PATH}/latest_release_assets.list"
CHECKSUMS_FILENAME="sqlitebiter_sha256.txt"

mkdir -p "${CACHE_DIR_PATH}"
curl -sSL https://raw.githubusercontent.com/thombashi/sqlitebiter/master/scripts/latest_release_assets.list > "${RELEASE_ASSETS}"

set +e
ARCHIVE_URL=$(cat "${RELEASE_ASSETS}" | \grep "${VERSION_CODENAME}_${ARCH}\.deb")
set -e

if [ "$ARCHIVE_URL" = "" ]; then
    echo "asset not found: CODENAME=${VERSION_CODENAME}, ARCH=${ARCH}" 1>&2
    exit 1
fi

DEB_FILENAME="$(basename ${ARCHIVE_URL})"
CACHE_FILE_PATH="${CACHE_DIR_PATH}/${DEB_FILENAME}"

TMP_DIR=$(mktemp -d)
cd "${TMP_DIR}"
trap 'rm -rf ${TMP_DIR}' 0 1 2 3 15

if [ -f "${CACHE_FILE_PATH}" ]; then
    echo "found local cache: ${DEB_FILENAME}"
    cp -a "${CACHE_FILE_PATH}" .
else
    echo "downloading a deb file ..."
    curl -fL --progress-bar "${ARCHIVE_URL}" -o "${DEB_FILENAME}"
fi

echo "check the file integrity ..."
CHECKSUMS_URL=$(cat "${RELEASE_ASSETS}" | \grep "${CHECKSUMS_FILENAME}")
curl -fsSL "${CHECKSUMS_URL}" -o "${CHECKSUMS_FILENAME}"
\grep "${DEB_FILENAME}" "${CHECKSUMS_FILENAME}" | sha256sum -c -

echo "installing ..."
dpkg -i "${DEB_FILENAME}"

# Replace the local cache file
cp -a "${DEB_FILENAME}" "${CACHE_FILE_PATH}"
