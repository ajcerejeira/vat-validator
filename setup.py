import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="vat-validator",
    version="0.1.0",
    author="Afonso Silva",
    author_email="ajcerejeira@gmail.com",
    description="VAT validation library",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ajcerejeira/vatval",
    license="MIT License",
    packages=setuptools.find_packages(),
    test_suite="tests",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
    ],
    install_requires=["zeep"],
)
