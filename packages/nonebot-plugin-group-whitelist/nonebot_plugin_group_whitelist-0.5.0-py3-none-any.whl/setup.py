# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(

    name="nonebot-plugin-group-whitelist",  ##模块名字

    version="0.6.0",  ##版本号

    packages=setuptools.find_packages(),

    author="轩某",  ##作者名字

    author_email="xuan_mou@outlook.com",  ##作者邮箱

    description="""适用于NoneBot2的群聊白名单""",  ##模块简介

    url="https://github.com/Rikka-desu/nonebot_plugin_group_whitelist",  ##模块链接

    install_requires=[  ##需要额外安装的模块

        "nonebot2>=2.0.0",  ##左边模块名字 右边版本号,
        "nonebot-plugin-localstore>=0.5.0"

    ],

    keywords=[],  ##关键词

    package_data={}

)
