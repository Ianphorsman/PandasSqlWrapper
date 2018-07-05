from setuptools import setup

setup(
    name='pandas-sql-wrapper',
    description="Tool to help pandas talk to mysql databases.",
    url="https://github.com/Ianphorsman/PandasSqlWrapper",
    author='Ian Horsman',
    author_email='ianphorsman@gmail.com',
    license='MIT',
    version='0.1.6',
    packages=['pandas_sql_wrapper'],
    install_requires=['numpy', 'pandas', 'pymysql', 'sqlalchemy']
)