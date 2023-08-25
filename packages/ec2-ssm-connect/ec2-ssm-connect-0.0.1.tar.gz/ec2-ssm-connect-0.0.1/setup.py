from setuptools import setup, find_packages

setup(
    name='ec2-ssm-connect',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='Ingo Marlos Batista de Sousa',
    description='An interactive command-line tool to list Amazon EC2 instances and establish secure connections using AWS Systems Manager (SSM) Session Manager.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',  # You can provide a repository or project URL here
    license='GPL-3.0',
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'ec2-ssm-connect=src.ec2_ssm_connect:main',  # Adjusted path
        ],
    },
    python_requires='>=3.9',
)

