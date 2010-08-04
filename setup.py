from setuptools import setup, find_packages
import os

version = '1.0'

setup(
    name='claytron.featuring',
    version=version,
    description="A console script to clean an iTunes library",
    long_description=open("README.txt").read() + "\n" +
                     open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      "Programming Language :: Python",
      ],
    keywords='itunes metadata',
    author='Clayton Parker',
    author_email='robots@claytron.com',
    url='http://claytron.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['claytron'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'appscript',
    ],
    entry_points="""
    [console_scripts]
    featuring_fix = claytron.featuring.script:main
    """,
    )
