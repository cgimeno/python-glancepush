#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.3                                                              #
# DESCRIPTION: Delete images from Cloud infrastructure using Openstack        #
#              API                                                            #
###############################################################################
import novaclient.v1_1.client as nvclient
import novaclient.exceptions
from clouds import get_nova_creds
from sys import exit
from os import environ

def delete_image(image_name):

    if environ['OS_IS_SECURE'] == "True":
        is_secure = True
    else:
        is_secure = False

    nova_credentials = get_nova_creds()
    nova = nvclient.Client(insecure=is_secure, **nova_credentials)
    try:
        image = nova.images.find(name=image_name)
        nova.images.delete(image.id)
        image_deleted = True
    except novaclient.exceptions.NotFound:
        image_deleted = False

    return image_deleted

def main():
    exit("You can't call this program directly")

if __name__ == "__main__":
    main()