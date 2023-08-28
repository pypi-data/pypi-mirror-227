#!/bin/bash
PREFIX=x86_64-w64-mingw32
export CC=$PREFIX-gcc-win32
export CPP=$PREFIX-cpp-win32
export RANLIB=$PREFIX-gcc-ranlib-win32
export AT=$PREFIX-gcc-ar-win32
exec "$@"
