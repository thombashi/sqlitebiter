if [ "$TRAVIS_OS_NAME" = "osx" ] && ! python3; then
    # Install Python3 on osx
    brew upgrade python
    pip3 install tox
else
    pip install tox
fi
