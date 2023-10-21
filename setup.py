from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="ivycheck",
    version="0.1.1",
    packages=find_packages(),
    # Include additional files into the package
    include_package_data=True,
    # Details
    url="http://pypi.PYPI.org/pypi/ivycheck/",
    # Author details
    author="Tammo Rukat, Dustin Lange",
    author_email="founders@deekard.com",
    # Choose your license
    license="MIT",
    # Long description read from the README.md
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    # Dependent packages (distributions)
    install_requires=required,
)
