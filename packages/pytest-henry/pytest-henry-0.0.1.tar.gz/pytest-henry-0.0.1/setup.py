

"""编写打包配置文件的信息的"""

# 这个是打包配置：编写项目打包的匹配信息的

from setuptools import setup

setup(
    name="pytest-henry",
    packages=["pytest_henry_plug"],
    version='0.0.1',
    # 配置pytest插件模块
    entry_points={"pytest11": ["pytest-henry = pytest_henry_plug.henry_plug"]},
    # pytest分类
    classifiers=["Framework :: Pytest"],
)


