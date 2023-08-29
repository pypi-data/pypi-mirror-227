import setuptools

setuptools.setup(
    name="taegis-magic",
    version="0.0.1-alpha",
    author="Secureworks",
    author_email="sdks@secureworks.com",
    description="Taegis IPython Magics",
    long_description="Dummy package for taegis-magic",
    long_description_content_type="text/markdown",
    url="https://github.com/secureworks/taegis-magics",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
