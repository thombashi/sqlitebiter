#!/bin/bash -x

set -eu

DIST_DIR_NAME="dist"
INSTALL_DIR_PATH="/usr/bin"
DIST_PATH="./${DIST_DIR_NAME}/${INSTALL_DIR_PATH}"
BIN_NAME="sqlitebiter"

# initialize
rm -rf $DIST_DIR_NAME
mkdir -p "${DIST_DIR_NAME}/DEBIAN"

pip install --upgrade .
PKG_VERSION=$(python -c "import pkg_resources; print(pkg_resources.get_distribution('${BIN_NAME}').version)")

echo $BIN_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --distpath $DIST_PATH --name $BIN_NAME

# build a deb package
cat << _CONTROL_ > "${DIST_DIR_NAME}/DEBIAN/control"
Package: $BIN_NAME
Version: $PKG_VERSION
Maintainer: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
Architecture: amd64
Description: $(cat docs/pages/introduction/summary.txt)
Homepage: https://github.com/thombashi/sqlitebiter
Priority: extra
_CONTROL_

fakeroot dpkg-deb --build $DIST_DIR_NAME $DIST_DIR_NAME
