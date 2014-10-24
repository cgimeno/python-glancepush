#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Software to upload images fetched from a VO image list         #
# using vmcatcher, to Openstack, using Openstack API.            #
# This software will                                             #
#                - Instanciate                                                #
#                - Apply policy checks                                        #
#                - Publish image if tests succeed                             #
#              Original software and idea by mpuel@in2p3.fr                   #
###############################################################################

import os
import sys
import tarfile
import stat
import argparse
import ConfigParser
from lib.delete import delete
from lib.clouds import init_openstack
import libcloud

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
    meta_directory = "/home/carlos"
    clouds_directory = "/etc/glancepush/clouds/"

    # Argument Parser options
    parser = argparse.ArgumentParser(description="Software to upload images fetched from a VO image list using.\n"
                                                 "vmcatcher, to Openstack, using Openstack API")
    parser.add_argument("--version", action="version", version="0.0.1")

    # Config Parser options
    config = ConfigParser.ConfigParser()
    cloud_config = ConfigParser.ConfigParser


    #if (os.path.isfile(cfg) == False):
    #    sys.exit("ERROR: Can't access config file")
    for cloud_file in os.listdir(clouds_directory):
        cloud_config.read(cloud_file)
        tenant = cloud_config.get("general", "testing_tenant")
        test_policy = cloud_config.get("general", "test_policy")
        cloud_username = cloud_config.get("general", "username")
        cloud_endpoint = cloud_config.get("general", "endpoint")
        cloud_password = cloud_config.get("general", "password")
        cloud_isendpointsecure = cloud_config.getboolean("general", "is_secure")
        cloud_type = cloud_config.get("general", "type")
        cloud_region = cloud_config.get("general", "region")
        cloud_service_name = cloud_config.get("general", 'service_name')
        if cloud_type == "Openstack":
            driver = init_openstack(cloud_username, cloud_password, cloud_endpoint, cloud_service_name,
                                    cloud_region, tenant, cloud_isendpointsecure)
        for file in os.listdir(meta_directory):
            with open(spooldir + file, "r") as image_file:
                line = image_file.readline()
                splitted = line.split("=")
                glance_image = splitted[1]
                if glance_image == "#DELETE#":
                    # Delete image from cloud
                    boolean = delete(driver, file)
                    if boolean:
                        print ("Image " + file + " deleted succsesfully")
                    boolean = delete(driver, file + ".q")

                    if boolean:
                        print("Image " + file + ".q deleted succsesfully")

                else:
                    pass
                image_file.close()

pass

if __name__ == "__main__":
    main()