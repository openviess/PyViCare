import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyViCare",
    version_config=True,
    author="Simon Gillet",
    author_email="mail+pyvicare@gillet.ninja",
    description="Library to communicate with the Viessmann ViCare API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somm15/PyViCare",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=['Authlib>=1.2.0'],
    setup_requires=['setuptools-git-versioning<1.8.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
