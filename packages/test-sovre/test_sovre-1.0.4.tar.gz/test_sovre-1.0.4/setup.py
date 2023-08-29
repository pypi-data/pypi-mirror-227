from distutils.core import setup
from setuptools import find_packages, setup

setup(
    name='test_sovre',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    version='1.0.4',
    license='MIT',
    description='Test package',
    author='Sovre',
    author_email="test@gmail.com",
    url='https://gitlab.com/udemy6864628/cicd/pypiexemple',
    download_url='https://gitlab.com/udemy6864628/cicd/pypiexemple/-/archive/0.1.0/pypiexemple-0.1.0.tar.gz',
    keywords=['test', 'package'],
    install_requires=[
    ],
    classifiers=[
		'Development Status :: 3 - Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers', # Define that your audience are developers
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License', # Again, pick a license
		'Programming Language :: Python :: 3', #Specify which pyhton versions that you want to support
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)