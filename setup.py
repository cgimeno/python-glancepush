from sys import version_info
import os

try:
    from setuptools import setup, find_packages
except ImportError:
	try:
            from distutils.core import setup
	except ImportError:
            from ez_setup import use_setuptools
            use_setuptools()
            from setuptools import setup, find_packages
            
version = "0.0.1"
productname = "python-glancepush"


data_files_installdir = "/usr/share/doc/gpvcmupdate-%s" % (version)
if "VIRTUAL_ENV" in  os.environ:
    data_files_installdir = 'doc'


setup(name=productname,
    version=version,
    description="%s upload images to OpenStack" % (productname),
    long_description="""Python-Glancepush is an implementation of glancepush using the native libraries of OpenStack. This work is based in the original implementation of Mattieu Puel)""",
    author="Carlos Gimeno Yanez",
    author_email="cgimeno@bifi.es",
    license='MIT License',
    url = 'https://github.com/cgimeno/python-glancepush',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],

    scripts=['glancepush.py'],
    packages=['pyglancepush'],
    data_files=[(data_files_installdir ,['README.md','ChangeLog','LICENSE'])]
    )