#!/usr/bin/python
import logging
import os
import pyrax
import sys


# Some constants we will replace via ansible
RACKSPACE_USERNAME = "{{ rackspace_username}}"
RACKSPACE_APIKEY = "{{ rackspace_apikey }}"
RACKSPACE_REGION = "{{ rackspace_region }}"

# Ensure we use a smaller segment size (250MB) for lower memory VM's
pyrax.object_storage.MAX_FILE_SIZE = 262144000

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Usage: Pass a VHD filename as the only argument")
    sys.exit(1)

vhd_file = sys.argv[1]

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", RACKSPACE_REGION)
pyrax.set_setting('debug', 'true')
pyrax.set_credentials(RACKSPACE_USERNAME, RACKSPACE_APIKEY)

files = pyrax.connect_to_cloudfiles(region=RACKSPACE_REGION, public=False)
imgs = pyrax.connect_to_images(region=RACKSPACE_REGION)

print("Ensuring image container exists...")
ctnr = files.create_container("images")

print("Uploading file...")
files_obj = ctnr.upload_file(os.path.basename(vhd_file))

print("Importing image...")
task = imgs.import_task(os.path.basename(vhd_file), 'images')

# NOTE(major): If you're having problems with your image imports, uncomment
# the following several lines so that you can get some output from your task.
pyrax.utils.wait_until(task, "status", ["success", "failure"],
        verbose=True, interval=15)
if task.status == "success":
    print("Success!")
else:
    print("Image import failed!")
    print("Reason: %s" % task.message)
