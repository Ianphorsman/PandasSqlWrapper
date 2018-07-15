<h1>PandasSQLWrapper</h1>
<h3>
    Provides upsert and schema updating capabilities when writing dataframes to existing sql tables.
    Currently works with mysql and postgres databases.
</h3>

<h4>Installation / Dependencies</h4>
<p>Dependencies: sqlalchemy, pymysql, pg8000</p>

'''bash

pip install pandas-sql-wrapper

'''

<h4>Getting Started</h4>
<p>
    Create an instance of PandasSQLWrapper supplying a database connection configuration.
    Either supply a dict or a string path to a json file as shown below.
</p>

'''python

sql_data = PandasSQLWrapper({
    host: '<host name>',
    db: '<database name>',
    user: '<database username>',
    password: '<database password'
})

sql_data = PandasSQLWrapper(configured_from='sql_config.json')

'''

<h4>Additional Options</h4>

'''python

sql_data = PandasSQLWrapper(
    configured_from='sql_config.json',
    postgres=False, # set to true if connecting to a postgres database
    verbose=False, # set to true for console logging of sql actions
    echo=False # set to true for sql database to communicate back performed actions
)

'''

<h4>Update Table</h4>
<p>
    Performs an upsert on a sql table and updates table schema by adding columns if necessary.
     Additionally, user can specify the option to remove rows and columns as part of the update.
     NOTE: The upsert is implemented differently depending on whether the database is mysql or postgres.
     For mysql, upsert is done using REPLACE INTO. For postgres, upsert is done using INSERT INTO ... ON CONFLICT.
</p>

'''python

    sql_data.update_table(
        '<table name>',
        df,
        permit_deletes=False # set to True if it is ok to delete rows or columns from sql table not found in dataframe
    )

'''

<h4></h4>