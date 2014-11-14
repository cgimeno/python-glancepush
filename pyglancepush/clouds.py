#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.5-devel                                                        #
# DESCRIPTION: Library to connect to Openstack                                #
# ##############################################################################

from sys import exit
from os import environ


def get_keystone_creds():
    """
    Reads keystone credentials from enviroment variables
    More info: http://www.ibm.com/developerworks/cloud/library/cl-openstack-pythonapis/
    :return: d. Dictionary with keystone credentials
    """
    d = {}
    d['username'] = environ['OS_USERNAME']
    d['password'] = environ['OS_PASSWORD']
    d['auth_url'] = environ['OS_AUTH_URL']
    d['tenant_name'] = environ['OS_TENANT_NAME']
    try:
        #Added support to cacert
        d['cacert'] = environ['OS_CACERT']
    except KeyError:
        pass
    return d

def get_nova_creds():
    """
    Reads nova credentials from enviroment variables
    More info: http://www.ibm.com/developerworks/cloud/library/cl-openstack-pythonapis/
    :return: d. Dictionary with nova credentials
    """
    d = {}
    d['username'] = environ['OS_USERNAME']
    d['api_key'] = environ['OS_PASSWORD']
    d['auth_url'] = environ['OS_AUTH_URL']
    d['project_id'] = environ['OS_TENANT_NAME']
    try:
        #Added support to cacert
        d['cacert'] = environ['OS_CACERT']
    except KeyError:
        pass
    return d


def main():
    exit("You can' call this python code directly")


if __name__ == "__main__":
    main()



