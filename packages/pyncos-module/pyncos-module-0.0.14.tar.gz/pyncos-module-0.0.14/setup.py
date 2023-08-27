#-*- coding:utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="pyncos-module", 
    version="0.0.14",   
    author="xuwh",  
    author_email="xuwhdev@gmail.com", 
    description="", 
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://gitee.com/zwsjz/carbot-module-lib", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
      'pyserial>=3.5',
      'paho-mqtt>=1.6.1'
    ]
)