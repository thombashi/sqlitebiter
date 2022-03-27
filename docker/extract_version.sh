#!/bin/sh

PACKAGE=sqlitebiter
TOPLEVEL_DIR=$(git rev-parse --show-toplevel)
VERSION_FILE=${PACKAGE}/__version__.py

cd "$TOPLEVEL_DIR"
VERSION=$(python3 -c "info = {}; exec(open('${PACKAGE}/__version__.py').read(), info); print(info['__version__'])")
echo "$VERSION"
