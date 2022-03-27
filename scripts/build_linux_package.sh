#!/usr/bin/env bash

set -eux

PYTHON=python3

ROOT_DIR=$(git rev-parse --show-toplevel)
DIST_DIR_NAME="dist"
DPKG_BUILD_DIR="dpkg_build"
INSTALL_DIR_PATH="/usr/local/bin"
BUILD_DIR_PATH="${ROOT_DIR}/${DPKG_BUILD_DIR}/${INSTALL_DIR_PATH}"
PKG_NAME="sqlitebiter"
SYSTEM=$($PYTHON -c "import platform; print(platform.system().casefold())")
ARCH=$(dpkg --print-architecture)

cd "$ROOT_DIR"

# initialize
rm -rf "$DIST_DIR_NAME" "$DPKG_BUILD_DIR" build
mkdir -p "${DPKG_BUILD_DIR}/DEBIAN" "$DIST_DIR_NAME"

pip install --upgrade "pip>=21.1"
pip install --upgrade .[all,buildexe]

PKG_VERSION=$($PYTHON -c "import ${PKG_NAME}; print(${PKG_NAME}.__version__)")

if [ "$PKG_VERSION" = "" ]; then
    echo 'failed to get the package version' 1>&2
    exit 1
fi

echo $PKG_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --distpath "$BUILD_DIR_PATH" --name $PKG_NAME
${BUILD_DIR_PATH}/${PKG_NAME} version

# build a deb package
cat << _CONTROL_ > "${DPKG_BUILD_DIR}/DEBIAN/control"
Package: $PKG_NAME
Version: $PKG_VERSION
Maintainer: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
Architecture: $ARCH
Description: $(cat docs/pages/introduction/summary.txt)
Homepage: https://github.com/thombashi/$PKG_NAME
Priority: extra
_CONTROL_
cat "${DPKG_BUILD_DIR}/DEBIAN/control"

fakeroot dpkg-deb --build "$DPKG_BUILD_DIR" "$DIST_DIR_NAME"
VERSION_CODENAME=$(\grep -Po "(?<=VERSION_CODENAME=)[a-z]+" /etc/os-release)
rename -v "s/_${ARCH}.deb/_${VERSION_CODENAME}_${ARCH}.deb/" ${DIST_DIR_NAME}/*

# generate an archive file
cd "$BUILD_DIR_PATH"
ARCHIVE_EXTENSION=tar.gz
SYSTEM=$($PYTHON -c "import platform; print(platform.system().casefold())")
ARCHIVE_FILE="${PKG_NAME}_${PKG_VERSION}_${SYSTEM}_${VERSION_CODENAME}_${ARCH}.${ARCHIVE_EXTENSION}"
tar -zcvf "$ARCHIVE_FILE" "$PKG_NAME"
mv "$ARCHIVE_FILE" "${ROOT_DIR}/${DIST_DIR_NAME}/"
