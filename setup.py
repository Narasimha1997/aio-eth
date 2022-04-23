
from setuptools import setup, find_packages

long_description = open('README.md').read()


setup(
    name='aio-eth',
    version='0.0.1',
    author='Narasimha Prasanna HN',
    author_email='narasimhaprasannahn@gmail.com',
    url='https://github.com/Narasimha1997/pyMigrate',
    description='A simple python library that can be used to run large Web3 ' +
        'queries on Ethereum blockchain concurrently as ' +
        'per Ethereum JSON-RPC specification.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    keywords='python web3 ethereum blockchain asyncio aio',
    zip_safe=False,
    install_requires=[
        "aiohttp==3.7.4.post0"
    ]
)
