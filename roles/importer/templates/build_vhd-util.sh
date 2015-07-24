#!/bin/bash

echo "*** Patching Xen source ***"
cd {{scratch_directory}}/xen-4.4.0/tools
cat {{scratch_directory}}/blktap2.patch | patch -p0 -N

echo "*** Running ./configure ***"
./configure --disable-monitors --disable-ocamltools --disable-rombios --disable-seabios 

echo "*** Compiling Xen source ***"
make -j4
make install