from setuptools import setup
import os

license_file = "LICENSE"
license_note = ""

if os.path.exists(license_file) is True:
    with open(license_file) as file:
        license_note = file.read();

setup(name="accounts",
      packages=["accounts", "accounts.server",
                "accounts.data",
                "accounts.repositories",
                'accounts.databases',
                'accounts.services',
                'accounts.validators'],
      version='1.0.12032020',
      description="beef_server implementation",
      url="https://github.com/miljimo/PyNodeGraph.git",
      author_email="johnson.obaro@hotmail.com",
      author="Obaro I. Johnson",
      license='Apache Licence 2.0',
      install_requires=['Flask'],
      classifiers=["Target Users : Developers"])
