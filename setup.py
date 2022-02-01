import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cilog",
    version="1.2.2",
    author="Shurui Gui",
    author_email="citrinegui@gmail.com",
    entry_points={
        'console_scripts': [
            'cilog=cilog.launcher:launcher'
        ]
    },
    description="CiLog is a flexible integrated logging tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CM-BF/CiLog/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas', 'tabulate', 'openpyxl'],
    python_requires='>=3.6',
)