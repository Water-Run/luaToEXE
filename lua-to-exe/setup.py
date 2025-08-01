from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lua-to-exe',
    version='1.0',
    install_requires=[],
    packages=find_packages(),
    author='WaterRun',
    author_email='2263633954@qq.com',
    description='Convert Lua scripts into standalone .exe executables with ready-to-use tools and libraries.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Water-Run/luaToEXE',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'lua_to_exe': ['srlua/**/*'],
    },
    entry_points={
        'console_scripts': [
            'lua-to-exe=lua_to_exe:gui',
        ],
    },
)
