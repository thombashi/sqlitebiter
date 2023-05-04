#!/usr/bin/env bash

set -eux

ROOT_DIR=$(git rev-parse --show-toplevel)
DIST_DIR_NAME="dist"
DIST_DIR_PATH="./${DIST_DIR_NAME}"
PKG_NAME="sqlitebiter"

if type python3 > /dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

$PYTHON --version

cd "$ROOT_DIR"

# initialize
rm -rf "$DIST_DIR_NAME" build

$PYTHON -m pip install --upgrade "pip>=21.1"
$PYTHON -m pip install --upgrade .[all,buildexe]

PKG_VERSION=$(${PYTHON} -c "import ${PKG_NAME}; print(${PKG_NAME}.__version__)")

if [ "$PKG_VERSION" = "" ]; then
    echo 'failed to get the package version' 1>&2
    exit 1
fi

echo $PKG_NAME $PKG_VERSION

# build an executable binary file
pyinstaller cli.py --clean --onefile --strip --distpath $DIST_DIR_PATH --name $PKG_NAME

# check the built binary file
${DIST_DIR_PATH}/${PKG_NAME} version

# generate an archive file
ARCH=$($PYTHON -c "import platform; machine=platform.machine().casefold(); print('amd64' if machine == 'x86_64' else machine)")

cd $DIST_DIR_PATH
ARCHIVE_FILE=${PKG_NAME}_macos_${ARCH}.tar.gz
tar -zcvf "$ARCHIVE_FILE" "$PKG_NAME"
# mv "$ARCHIVE_FILE" "${ROOT_DIR}/${DIST_DIR_NAME}/"
