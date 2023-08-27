# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="ai-service-wrapper",
    version="0.0.a",
    description="Just for ai service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Engreed68",
    author_email="trungpn@apero.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["ai_service_wrapper"],
    include_package_data=True,
    install_requires=[
        "cryptography==41.0.3",
        "Flask==2.3.3",
        "prometheus-client==0.17.1",
        "pytest==7.4.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0"
    ]
)