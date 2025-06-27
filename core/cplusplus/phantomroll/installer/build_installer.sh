#!/bin/bash
# Build C++ shared library for PhantomRoll

cd "$(dirname "$0")/../core/cplusplus" || exit 1
g++ -shared -fPIC -o libphantomroll.so message_deleter.cpp

echo "✅ C++ shared library built: libphantomroll.so"
