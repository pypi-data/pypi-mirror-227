#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Name:  setup
@IDE：PyCharm
@Author:qtclm
@Date：2023/8/26 16:23
'''


import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '1.0.1'
DESCRIPTION = '个人项目常用工具类'

setup(
    # name="要显示的唯一标识（用于pip install xxx）",
    name="turtle_utils",
    version=VERSION,
    author="qtclm",
    author_email="248313385@qq.com",
    description=DESCRIPTION,
    # 长描述内容的类型设置为markdown
    long_description_content_type="text/markdown",
    # 长描述设置为README.md的内容
    long_description=long_description,
    # 使用find_packages()自动发现项目中的所有包
    packages=find_packages(),
    # 许可协议
    license='MIT',
    # 要安装的依赖包
    install_requires=[
        # "Faker>=18.7.0",
        # "ddddocr>=1.4.7",
        # "requests>=2.30.0",
        # "loguru>=0.7.0",
        # "lxml>=4.9.2",
    ],
    # keywords=['python', 'menu', 'dumb_menu','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
