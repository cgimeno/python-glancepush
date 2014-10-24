#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Library to connect to different clouds                         #
# ##############################################################################
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import sys


def init_openstack(cloud_username, cloud_password, cloud_endpoint, service, region, tenant, cloud_isendpointsecure):
    """
    Initiates a connection with Openstack cloud. Returns driver if successful
    :param tenant:
    :param cloud_username:
    :param cloud_endpoint:
    :param cloud_password:
    :param cloud_isendpointsecure:
    :param region:
    :return:
    """

    if cloud_isendpointsecure:
        libcloud.security.VERIFY_SSL_CERT = True
    else:
        libcloud.security.VERIFY_SSL_CERT = False

    openstack = get_driver(Provider.OPENSTACK)
    driver = openstack(cloud_username, cloud_password, ex_force_auth_url=cloud_endpoint,
                       ex_force_auth_version='2.0_password',
                       ex_force_service_type='compute', ex_force_service_name=service, ex_force_service_region=region,
                       ex_tenant_name=tenant)
    return driver
    pass

# TODO: Implement more methods to support more clouds

def main():
    sys.exit("You can' call this python code directly")


if __name__ == "__main__":
    main()



