#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Create a new instance, and runs policy checks on it            #
###############################################################################
import os
import time
import novaclient.v1_1.client as nvclient
from clouds import get_nova_creds
from sys import exit
import paramiko

__author__ = "Carlos Gimeno"
__license__ = "MIT"
__maintainer__ = "Carlos Gimeno"
__email__ = "cgimeno@bifi.es"
__status__ = "Development"


def policy_check(ssh_key, image_name):

    if os.environ['OS_IS_SECURE'] == "True":
        secure = True
    else:
        secure = False

    credentials = get_nova_creds()
    nova = nvclient.Client(insecure=secure, **credentials)
    if not nova.keypairs.findall(name=ssh_key):
        # We're going to create a new ssh key if we can't find the one supplied by the user
        print "Keypair not found. Creating a new one keypair..."
        keypair = nova.keypairs.create(name=ssh_key)

    image_to_use = nova.images.find(name=image_name)
    # We're going to use a medium flavor, just to be sure that we can successfully create an instance.
    flavor_to_use = nova.flavors.find(name="m1.medium")
    instance = nova.servers.create(name=image_name + ".policy", image=image_to_use, flavor=flavor_to_use,
                                   key_name=ssh_key)
    # Poll at 20 second intervals (a bit conservative), until the status is 'ACTIVE'
    status = instance.status
    while status == 'BUILD':
        time.sleep(20)
        # Retrieve the instance again to update the status field
        instance = nova.servers.get(instance.id)
        status = instance.status
    # Add a new floating ip to the instance
    floating_ip = nova.floating_ips.create()
    instance.add_floating_ip(floating_ip)
    ssh = paramiko.SSHClient
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=floating_ip, port=22, username=root, key_filename="/home/carlos/.ssh/id_rsa.pub")
    ssh.exec_command('mkdir -p /tmp/tests/')
    ftp = ssh.open_sftp()
    ftp.put('/etc/glancepush/test/Basic_Ubuntu_Server_12.04_LTS_OS_Disk_Image', '/tmp/tests')
    ssh.exec_command('chmod a+x /tmp/tests/Basic_Ubuntu_Server_12.04_LTS_OS_Disk_Image')
    ssh.exec_command('/tmp/tests/Basic_Ubuntu_Server_12.04_LTS_OS_Disk_Image')
    nova.servers.delete(instance.id)
    nova.floating_ips.delete(floating_ip)


def main():
    exit("You can't call this program directly")


if __name__ == "__main__":
    main()


