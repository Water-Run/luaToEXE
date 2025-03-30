from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lua-to-exe',  # 包名称（pip 安装时使用）
    version='0.1',  # 当前版本号
    install_requires=[],  # 依赖项列表
    packages=find_packages(),  # 自动发现包（会找到 lua_to_exe）
    author='WaterRun',  # 作者名
    author_email='2263633954@qq.com',  # 作者邮箱
    description='Convert Lua scripts into standalone .exe executables with ready-to-use tools and libraries.',  # 简要描述
    long_description=long_description,  # 长描述，通常是 README.md 内容
    long_description_content_type='text/markdown',  # 长描述格式为 Markdown
    url='https://github.com/Water-Run/luaToEXE',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',  # Python 版本要求
    include_package_data=True,  # 包含其他数据文件
    package_data={
        'lua_to_exe': ['srlua/*'],  # 包含 srlua 目录下的所有文件
    },
    entry_points={
        'console_scripts': [
            'lua-to-exe=lua_to_exe:gui',  # 命令行入口点
        ],
    },
)