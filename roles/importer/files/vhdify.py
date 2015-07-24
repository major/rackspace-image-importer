#!/usr/bin/env python
import os
import shlex
import subprocess
import sys
import time


image_path = sys.argv[1]
filename = os.path.basename(image_path)
(filename_bare, extension) = os.path.splitext(filename)

# If we have a QCOW image, we need to convert to raw first.
if extension.startswith('.qcow'):
    command = "qemu-img convert {0} {1}.{2}".format(filename,
                                                    filename_bare,
                                                    'raw')
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.wait()
    time.sleep(5)

# Convert to vhd
commands = [
    "vhd-util convert -s 0 -t 1 -i {0}.{1} -o {0}.{1}".format(filename_bare,
                                                              'raw'),
    "vhd-util convert -s 1 -t 2 -i {0}.{1} -o {0}.{2}".format(filename_bare,
                                                              'raw',
                                                              'vhd')
]
for command in commands:
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.wait()

print("{0}.{1}".format(filename_bare, 'vhd'))
