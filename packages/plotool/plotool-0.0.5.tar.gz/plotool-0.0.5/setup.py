from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Useful tools for plotting'
LONG_DESCRIPTION = 'Realtime to plot data'

# 配置
setup(
    name="plotool",
    version=VERSION,
    author="Xinlin Wang",
    author_email="wangxinlin525@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "matplotlib",
    ],
    keywords=['python', 'plot'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)