#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.3                                                              #
# DESCRIPTION: Upload images to the cloud using Openstack API                 #
# ##############################################################################
from clouds import *
from pyglancepush.delete import delete_image
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as nvclient
import novaclient.exceptions
import logging
import json
import glanceclient
from sys import exit
from os import environ

__author__ = "Carlos Gimeno"
__license__ = "MIT"
__maintainer__ = "Carlos Gimeno"
__email__ = "cgimeno@bifi.es"
__status__ = "Development"


def publish_image(image_file, image_name, image_format, container_format, is_public, is_protected, properties_dict):
    """
    Publish image into quarantine area
    :param image_file:
    :param image_name:
    :param image_format:
    :param container_format:
    :param properties_dict:
    :return:
    """
    logger = logging.getLogger('glancepush')
    if environ['OS_IS_SECURE'] == "True":
        is_secure = True
    else:
        is_secure = False

    if is_public == "\"yes\"":
        public = True
    else:
        public = False

    if is_protected == "\"yes\"":
        protect_image = True
    else:
        protect_image = False
    # Before doing anything else, check if this image is associated with current VO
    File_Open = False
    try:
        json_file = open("/etc/glancepush/voms.json").read()
        File_Open = True
    except IOError:
        logger.critical("CRITICAL ERROR! /etc/glancepush/voms.json is not accessible")
    if File_Open:
        json_data = json.loads(json_file)
        VO = properties_dict['VMCATCHER_EVENT_VO']
        try:
            tenant_VO = json_data[VO]["tenant"]
            if tenant_VO != environ['OS_TENANT_NAME'] :
                logger.info("This image is not associated with the current VO")
                logger.info("Current VO is " + environ['OS_TENANT_NAME'] + "image VO is " + tenant_VO)
                logger.info("Skipping image " + image_name)
                return
        except KeyError:
            logger.critical("CRITICAL ERROR! Tenant " + VO + " not defined in voms.json file")

        else:
            # Process image
            json_file = open("/etc/glancepush/voms.json").read()
            json_data = json.loads(json_file)
            credentials = get_keystone_creds()
            nova_credentials = get_nova_creds()
            nova = nvclient.Client(insecure=is_secure, **nova_credentials)
            keystone = ksclient.Client(insecure=is_secure, **credentials)
            glance_endpoint = keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            glance = glanceclient.Client('1', glance_endpoint, token=keystone.auth_token, insecure=is_secure)
            found = False
            upload = True
            logger.info('Proccessing '+ image_name)
            try:
                # Check if image has been already uploaded.
                image = nova.images.find(name=image_name)
                found = True
            except novaclient.exceptions.NotFound:
                pass
            # If image exists, get his metadata
            if found:
                metadata = nova.images.get(image.id).metadata
                old_version = metadata['vmcatcher_event_hv_version']
                new_version = properties_dict['VMCATCHER_EVENT_HV_VERSION']
                VO = properties_dict['VMCATCHER_EVENT_VO']
                if old_version == new_version:
                    logger.info("Skipping image " + image_name + " version number " + new_version + " is the same in the stored image")
                    upload = False
                else:
                    try:
                        logger.info("New version found: " + new_version)
                        logger.info("Uploading to tenant: " + json_data[VO]["tenant"])
                        logger.info("Deleting previous version...")
                        logger.info("Uploading new version")
                        delete = delete_image(image_name)
                    except KeyError:
                        logger.critical("CRITICAL ERROR! Tenant " + VO + " not defined in voms.json file")
            else:
                logger.info("Uploading to tenant: " + json_data[VO]["tenant"])
            if upload:
                with open(image_file, 'r') as fimage:
                    image = glance.images.create(name=image_name, disk_format=image_format,
                                                 container_format=container_format,
                                                 data=fimage, properties=properties_dict, is_public=public, protected=protect_image)
            if upload:
                print nova.images.get(image.id).metadata


def main():
    exit("You can't call this program directly")


if __name__ == "__main__":
    main()
