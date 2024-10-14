"""Module to setup the orderful api package. """

from setuptools import setup, find_packages

setup(
    name='orderful',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'urllib3', 'requests'
        # Add your project's dependencies here
        # e.g., 'requests', 'numpy', etc.
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
            # e.g., 'orderful-api=orderful_api.cli:main',
        ],
    },
    author='Pete Snyder',
    author_email='psnyder@cybernexus-solutions.com',
    description='Python library for the Orderful API',
    long_description=open(file='README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cybernexus-Solutions/orderful-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)