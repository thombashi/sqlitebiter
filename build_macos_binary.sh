#!/usr/bin/env bash

set -eux

DIST_DIR_NAME="dist"
DIST_DIR_PATH="./${DIST_DIR_NAME}"
PKG_NAME="sqlitebiter"

# initialize
rm -rf $DIST_DIR_NAME

pip install --upgrade pip
pip install --upgrade .[build]
PKG_VERSION=$(python -c "import ${PKG_NAME}; print(${PKG_NAME}.__version__)")

if [ "$PKG_VERSION" = "" ]; then
    echo 'failed to get the package version' 1>&2
    exit 1
fi

echo $PKG_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --distpath $DIST_DIR_PATH --name $PKG_NAME

# generate an archive file
cd $DIST_DIR_PATH
tar -zcvf "sqlitebiter_macos_amd64.tar.gz" .
