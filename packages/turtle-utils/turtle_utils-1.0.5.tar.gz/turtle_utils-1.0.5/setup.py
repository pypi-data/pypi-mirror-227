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
from turtle_utils.other_util import get_project_rootpath

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# you need to change all these
VERSION = '1.0.5'
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
        "allpairspy==2.5.0",
        "cryptography==3.4.8",
        "Faker==12.0.1",
        "jsonpath_rw==1.4.0",
        "jsonpath_rw_ext==1.2.2",
        "loguru==0.6.0",
        "openpyxl==3.1.0",
        "oss2==2.15.0",
        "passlib==1.7.4",
        "pycryptodome==3.18.0",
        "pymongo==4.0.2",
        "PyMySQL==0.10.1",
        "python_dateutil==2.8.2",
        "pytz==2021.1",
        "redis==3.5.3",
        "requests==2.28.2",
        "ruamel.base==1.0.0",
        "tabulate==0.8.9",
        "XlsxWriter==3.0.8",
        "xpinyin==0.7.6",
        "twine==4.0.1"
    ],
    keywords=['python', 'qtclm','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
