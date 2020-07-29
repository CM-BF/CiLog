import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cilog",
    version="0.0.2",
    author="Shurui Gui",
    author_email="citrinegui@gmail.com",
    description="CiLog is a flexible integrated logging tool base on package logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CM-BF/CiLog/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)