#!/usr/bin/env bash

set -eux

DIST_DIR_NAME="dist"
INSTALL_DIR_PATH="/usr/bin"
DIST_DIR_PATH="./${DIST_DIR_NAME}/${INSTALL_DIR_PATH}"
PKG_NAME="sqlitebiter"

# initialize
rm -rf $DIST_DIR_NAME
mkdir -p "${DIST_DIR_NAME}/DEBIAN"

pip install --upgrade pip>=19.0.2
pip install --upgrade .[excel,gs,mediawiki,sqlite,buildexe]

PKG_VERSION=$(python -c "import ${PKG_NAME}; print(${PKG_NAME}.__version__)")

if [ "$PKG_VERSION" = "" ]; then
    echo 'failed to get the package version' 1>&2
    exit 1
fi

echo $PKG_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --distpath $DIST_DIR_PATH --name $PKG_NAME

# build a deb package
cat << _CONTROL_ > "${DIST_DIR_NAME}/DEBIAN/control"
Package: $PKG_NAME
Version: $PKG_VERSION
Maintainer: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
Architecture: amd64
Description: $(cat docs/pages/introduction/summary.txt)
Homepage: https://github.com/thombashi/sqlitebiter
Priority: extra
_CONTROL_

fakeroot dpkg-deb --build $DIST_DIR_NAME $DIST_DIR_NAME
