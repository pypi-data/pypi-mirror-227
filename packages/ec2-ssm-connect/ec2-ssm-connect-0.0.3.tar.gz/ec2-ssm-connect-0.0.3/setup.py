from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Read the README.md for the long description
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Define the version, descriptions, etc.
VERSION = '0.0.3'
DESCRIPTION = 'An interactive command-line tool to list Amazon EC2 instances and establish secure connections using AWS Systems Manager (SSM) Session Manager.'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    name="ec2-ssm-connect",
    version=VERSION,
    author="Ingo Marlos Batista de Sousa",
    author_email="",  # You can add an email here if you want
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://www.github.com/ingomarlos/ec2-ssm-connect",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['boto3'],
    keywords=['python', 'aws', 'ec2', 'ssm', 'systems manager', 'session manager'],
    entry_points={
        'console_scripts': [
            'ec2-ssm-connect=src.ec2_ssm_connect:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.9',
)

