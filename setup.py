import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyViCare",
    version="0.0.2",
    author="Simon Gillet",
    author_email="mail+pyvicare@gillet.ninja",
    description="Library to communicate with the Viessmann ViCare API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somm15/PyViCare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
)