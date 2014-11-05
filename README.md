Python-Glancepush
================

Python-Glancepush is an implementation of glancepush using the native libraries of OpenStack. This work is based in the original implementation of Mattieu Puel. You can find the original implementation [here](https://github.com/EGI-FCTF/glancepush).

Requirements:

 - Python 2.7.3 (Tested)
 - [vmcatcher 0.5.4](https://github.com/hepix-virtualisation/vmcatcher)
 - [Openstack handler for vmcatcher 0.0.4](https://github.com/cgimeno/Openstack-handler-for-vmcatcher)
 - python-novaclient
 - python-glanceclient

----

Installation Instructions
===================

You have 3 options:

 - Clone this repository. After that, go into cloned directory and execute "python setup.py install"
 - Download it from [Releases](https://github.com/cgimeno/python-glancepush/releases) page
 - Download it from [yokel.org](http://www.yokel.org/pub/software/yokel.org/release/x86_64/scientific/6x/rpm/). Thanks to Owen Synge


---

Usage
========
First of all, you will need /etc/keystone/voms.json, the file which maps VO's and tenants. Copy it to /etc/glancepush/voms.json

This software will use the same files that glancepush (/var/spool/, /etc/glancepush/meta)

You'll need to create some files in clouds directory. You'll need a file per site and VO (tenant).
For example if your site is some_site and you have in your voms.json the following:

	{
    "fedcloud.egi.eu": {
        "tenant": "egi"
    },
    "ops": {
        "tenant": "ops"
    },
    "biomed.eu": {
        "tenant": "biomed"
    },
    "dteam": {
        "tenant": "dteam"
    }
	   }

Create two files, one for fedcloud.egi.eu, and another one for biomed.eu following this structure:

	[general]
	# Tenant for this VO. Must match the tenant defined in voms.json file
	testing_tenant=egi
	# Identity service endpoint (Keystone)
	endpoint_url=https://server4-eupt.unizar.es:5000/v2.0
	# User Password
	password=123456
	# User
	username=John
	# Set this to true if you're NOT using self-signed certificates
	is_secure=True
	# SSH private key that will be used to perform policy checks (to be done)
	ssh_key=Carlos_lxbifi81
	# WARNING: Only define the next variable if you're going to need it. Otherwise you may encounter problems
    cacert=path_to_your_cert

Finally, just run glancepush.py **(python glancepush.py)**

---

TO-DO
--------

 - Add policy checks
 - Clear /var/spool/glancepush directory after uploading images (it's this neccesary?)
 - Clear /tmp after uploading

 