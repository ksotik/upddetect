#!/bin/bash
VERSION=`cat ./upddetect/variables.py | grep "__VERSION__" | awk -F '"' '{print $2;}'`
MKDIR=`which mkdir`
PYTHON=`which python3`
PIP=`which pip3`

$PIP install nuitka
$MKDIR -p bin
$PYTHON -m nuitka --standalone --onefile --product-name=upddetect --product-version=$VERSION --output-dir=./bin --output-filename=upddetect.bin ./upddetect/upddetect_app.py
