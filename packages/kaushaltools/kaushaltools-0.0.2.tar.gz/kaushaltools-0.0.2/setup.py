from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Making Simple to use tools with easy commands'
LONG_DESCRIPTION = 'A package thet allow to simpley use of different tools'
KEYWORDS = ['python', 'tools', 'qrcode', 'encryption', 'data encrypt', 'show qr code']
REQUIRED_PACKAGES = ['qrcode', 'opencv-python', 'cryptography', 'json', 'pyotp']


# Setting up
setup(
    name="kaushaltools",
    version=VERSION,
    author="Kaushal Bhatol",
    author_email="kaushal@bhatol.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    keywords=KEYWORDS,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

