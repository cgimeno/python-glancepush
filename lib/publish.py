#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Upload images to the cloud using Openstack API                 #
###############################################################################
from clouds import get_keystone_creds
import keystoneclient.v2_0.client as ksclient
import glanceclient
from sys import exit
from os import environ

__author__ = "Carlos Gimeno"
__license__ = "MIT"
__maintainer__ = "Carlos Gimeno"
__email__ = "cgimeno@bifi.es"
__status__ = "Development"

def publish_image(image_file, image_name, image_format, container_format, properties_dict):
    """
    Publish image into quarantine area
    :param image_file:
    :param image_name:
    :param image_format:
    :param container_format:
    :param properties_dict:
    :return:
    """
    if environ['OS_IS_SECURE'] == "True":
        is_secure = True
    else:
        is_secure = False

    credentials = get_keystone_creds()
    keystone = ksclient.Client(insecure=is_secure, **credentials)
    glance_endpoint = keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
    glance = glanceclient.Client('1',glance_endpoint, token=keystone.auth_token)
    with open(image_file, 'r') as fimage:
        glance.images.create(name=image_name+".q", disk_format="qcow2", container_format="bare",
                             data=fimage, properties =  properties_dict )

def main():
    exit("You can't call this program directly")

if __name__ == "__main__":
    main()