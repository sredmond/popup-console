"""Graphical Popup Console in Python"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open  # Default to text mode with universal newlines.

# Load the text of the README file.
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='popup-console',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='A graphical popup console in Python with TK.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    # url='https://sredmond.io',

    # Author details
    author='Sam Redmond',
    author_email='sredmond@stanford.edu',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        # Other classifiers
        'Natural Language :: English',
        # 'Operating System :: MacOS',
        # 'Operating System :: Microsoft',
        # 'Operating System :: Unix',
    ],

    # What does your project relate to?
    keywords='popup console graphics graphical',

    # Specific package directories.
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Distribrute a single Python file named console.py.
    # py_modules=['console'],

    # Supported Python versions. Unlike the classifiers, `pip install` actually
    # checks these constraints and refuses to install projects with mismatches.
    # python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    # Run-time dependencies.
    # See: https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # Additional (development) dependency groups.
    # To install these, use the following syntax:
    #     pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest'],
    },

    # Additional URLs.
    project_urls= {
        'Source': 'https://github.com/sredmond/popup-console/',
        'Bug Reports': 'https://github.com/sredmond/popup-console/issues',
        'Say Thanks!': 'http://saythanks.io/to/sredmond',
        # 'Funding': 'https://donate.pypi.org',
    },
)
