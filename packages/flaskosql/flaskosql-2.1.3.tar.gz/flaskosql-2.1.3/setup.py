from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.1.3'
DESCRIPTION = 'ORM to databases for FLASK API'
LONG_DESCRIPTION = 'An ORM that allow us to connect with the relational databases (ORACLE and MySQL) using OOP concept, plus the interaction with the database in order to create a rest API using FLASK framwork '

# Setting up
setup(
    name="flaskosql",
    version=VERSION,
    author="Ashraf khabar",
    author_email="<khabarachraf@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['cx_Oracle', 'mysql-connector-python'],
    keywords=['python', 'orm', 'api', 'oracle', 'mysql', 'database', 'flask'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
