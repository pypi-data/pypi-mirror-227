from setuptools import setup, find_packages

setup(
    name='ssa-gov',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'beautifulsoup4',
        'html5lib',
        'fake_useragent'
    ],
    author='Roberto Banić @ Octris LLC',
    author_email='roberto@octr.is',
    description='A library enabling users to fetch data from ssa.gov.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git.octr.is/open-source/data/ssa-gov',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)