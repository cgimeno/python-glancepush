#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Software to upload images fetched from a VO image list         #
#              using vmcatcher, to Openstack, using Openstack API.            #
#              This software will                                             #
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

    # Argument Parser options
    parser = argparse.ArgumentParser(description="Software to upload images fetched from a VO image list using.\n"
                                                 "vmcatcher, to Openstack, using Openstack API")
    parser.add_argument("--version", action="version", version="0.0.1")

    # Config Parser options
    config = ConfigParser.ConfigParser()


    #if (os.path.isfile(cfg) == False):
    #    sys.exit("ERROR: Can't access config file")

    for file in os.listdir(meta_directory):
        with open(spooldir + file,"r") as image_file:
            line = image_file.readline()
            splitted = line.split("=")
            glance_image = splitted[1]





pass

if __name__ == "__main__":
    main()