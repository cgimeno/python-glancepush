#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Software to upload images fetched from a VO image list         #
# using vmcatcher, to Openstack, using Openstack API.                         #
# This software will                                                          #
#                - Instanciate                                                #
#                - Apply policy checks                                        #
#                - Publish image if tests succeed                             #
#              Original software and idea by mpuel@in2p3.fr                   #
###############################################################################

import os
import argparse
import ConfigParser
import re
from lib.delete import delete_image
from lib.publish import publish_image
from lib.policy import policy_check

__author__ = "Carlos Gimeno"
__license__ = "MIT"
__maintainer__ = "Carlos Gimeno"
__email__ = "cgimeno@bifi.es"
__status__ = "Development"


def main():
    # Logging

    # Configuration directories

    cfg = "/etc/glancepush/glancepushrc"
    spooldir = "/var/spool/glancepush/"
    meta_directory = "/etc/glancepush/meta/"
    clouds_directory = "/etc/glancepush/clouds/"

    # Argument Parser options

    parser = argparse.ArgumentParser(description="Software to upload images fetched from a VO image list using.\n"
                                                 "vmcatcher, to Openstack, using Openstack API")
    parser.add_argument("--version", action="version", version="0.0.1")

    # Config Parser options

    cloud_config = ConfigParser.ConfigParser()

    for cloud_file in os.listdir(clouds_directory):
        # Read configuration file for every cloud in clouds directory
        cloud_config.read(clouds_directory + cloud_file)
        tenant = cloud_config.get("general", "testing_tenant")
        auth_url = cloud_config.get("general", "endpoint_url")
        password = cloud_config.get("general", "password")
        username = cloud_config.get("general", "username")
        is_secure = cloud_config.get("general", "is_secure")
        ssh_key = cloud_config.get("general", "ssh_key")

        # Set the enviroment variables for keystone and nova-client
        os.environ['OS_USERNAME'] = username
        os.environ['OS_PASSWORD'] = password
        os.environ['OS_AUTH_URL'] = auth_url
        os.environ['OS_TENANT_NAME'] = tenant
        os.environ['OS_IS_SECURE'] = is_secure


        # And for every clouds, in clouds directory, we are going to upload (or delete) all images in meta directory
        # To do this, we're going to read all files in meta directory, open their equivalent in spool directory
        # and we're going to process these files.
        for files in os.listdir(meta_directory):
            with open(spooldir + files, "r") as image_file:
                line = image_file.readline()
                splitted = line.split("=")
                glance_image = splitted[1]
                if glance_image == "\'#DELETE#\'":
                    print files
                    # Delete image from cloud infrastructure
                    deleted = delete_image(files)
                    if deleted:
                        print "Image " + files + "deleted"
                    else:
                        print "Image not found, or has been already deleted"
                else:
                    # We're going to upload the image to the infrastructure
                    with open(meta_directory + files,"r") as meta_file:
                        properties_dict = {}
                        ab = re.compile("properties\[\d+\]")
                        image_format = "qcow2"
                        container_format = "bare"
                        for line in meta_file:
                            splitted = line.split("=")
                            if splitted[0] == 'comment':
                                properties_dict['comment'] = splitted[1].rstrip('\n').replace('\'', '')

                            elif splitted[0] == "disk_format":
                                image_format = splitted[1].replace('\"', '')

                            elif splitted[0] == "container_format":
                                container_format = splitted[1].replace('\"', '')

                            elif splitted[0] == "is_public":
                                is_public = splitted[1].rstrip('\n')

                            elif splitted[0] == "is_protected":
                                is_protected = splitted[1].rstrip('\n')

                            elif ab.match(splitted[0]):
                                key = splitted[1].replace('\'', '')
                                value = splitted[2].rstrip('\n').replace('\'', '')
                                properties_dict[key] = value
                        # Publish image into quarantine area
                        publish_image(glance_image, files, image_format, container_format, is_public, is_protected, properties_dict)
                        # TODO Finish policy check
                        #policy_check(ssh_key, files)
                    meta_file.close()
            image_file.close()

if __name__ == "__main__":
    main()
