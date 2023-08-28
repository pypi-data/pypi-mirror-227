from setuptools import setup, find_packages
import twine

VERSION = '0.0.1'
DESCRIPTION = 'A namemc package'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="namemcscrape",
    version=VERSION,
    author="Issac",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['namemc', 'minecraft', 'scraper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)