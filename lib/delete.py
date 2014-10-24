#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
# AUTHOR: Carlos Gimeno                                                       #
# EMAIL: cgimeno@bifi.es                                                      #
# VERSION: 0.0.1                                                              #
# DESCRIPTION: Delete images from  Cloud                                      #
###############################################################################
import libcloud
import libcloud.security
import sys

def delete(driver, name):
    boolean = driver.delete_image(name)
    return boolean
    pass



def main():
    sys.exit("You can't call this program directly")



if __name__ == "__main__":
    main()