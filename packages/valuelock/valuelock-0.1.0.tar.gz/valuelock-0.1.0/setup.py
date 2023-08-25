from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Package metadata
NAME = 'valuelock'
VERSION = '0.1.0'  # Suggested starting version
DESCRIPTION = 'A Python package for locking based on values.'
AUTHOR = 'killbus'
EMAIL = 'killbus@users.noreply.github.com'
URL = 'https://github.com/killbus/py-valuelock'

# Define package dependencies, if any
INSTALL_REQUIRES = [
    # Add your dependencies here
]

# Package setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,  # Use the README as long description
    long_description_content_type="text/markdown",  # Specify the content type
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
