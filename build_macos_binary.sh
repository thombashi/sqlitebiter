#!/usr/bin/env bash

set -eux

DIST_DIR_NAME="dist"
DIST_DIR_PATH="./${DIST_DIR_NAME}"
PKG_NAME="sqlitebiter"

python --version
echo $(python -c "from __future__ import print_function; import sys; print(sys.version_info[0])")

if type python3 > /dev/null 2>&1; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

# initialize
rm -rf $DIST_DIR_NAME

$PIP install --upgrade pip>=19.0.2 jsonschema==2.6.0
$PIP install --upgrade .[excel,gs,mediawiki,sqlite,buildexe]

PKG_VERSION=$(${PYTHON} -c "import ${PKG_NAME}; print(${PKG_NAME}.__version__)")

if [ "$PKG_VERSION" = "" ]; then
    echo 'failed to get the package version' 1>&2
    exit 1
fi

echo $PKG_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --distpath $DIST_DIR_PATH --name $PKG_NAME

# generate an archive file
cd $DIST_DIR_PATH
ARCHIVE_FILE=sqlitebiter_macos_amd64.tar.gz
tar -zcvf "$ARCHIVE_FILE" "$PKG_NAME"
shasum -a 256 "$ARCHIVE_FILE" > "${PKG_NAME}_macos_sha256.txt"
