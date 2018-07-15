from setuptools import setup

setup(
    name='pandas-sql-wrapper',
    description="Tool to help pandas talk to mysql or postgresql databases." +
                "Introduces upsert and schema updating capabilities when writing dataframes to sql tables.",
    url="https://github.com/Ianphorsman/PandasSqlWrapper",
    author='Ian Horsman',
    author_email='ianphorsman@gmail.com',
    license='MIT',
    version='0.2.0',
    packages=['pandas_sql_wrapper'],
    install_requires=['numpy', 'pandas', 'pymysql', 'sqlalchemy', 'pg8000']
)