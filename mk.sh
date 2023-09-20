#!/usr/bin/env bash

set -u
set -e

LOCAL_PATH=`pwd`
OUT_PATH=$1
BUILD_TYPE=$2

# ----------------------------------------------------------------
# build
# ----------------------------------------------------------------
python build.py $OUT_PATH $BUILD_TYPE
