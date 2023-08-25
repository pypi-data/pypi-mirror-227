from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'An interactive command-line tool to list Amazon EC2 instances and establish secure connections using AWS Systems Manager (SSM) Session Manager.'


setup(
    name="ec2-ssm-connect",
    version=VERSION,
    packages=find_packages(),
    install_requires=['boto3'],
    entry_points={
        'console_scripts': [
            'ec2-ssm-connect=ec2_ssm_connect.main:main',
        ],
    },
    author="Ingo Marlos Batista de Sousa",
    author_email="your.email@example.com",
    keywords=['aws', 'ec2', 'ssm', 'systems manager', 'session manager'],
    description=DESCRIPTION,
    url="https://www.github.com/ingomarlos/ec2-ssm-connect",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
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