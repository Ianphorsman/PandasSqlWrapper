<h1>PandasSQLWrapper</h1>
<h4>
    Provides upsert and schema updating capabilities when writing dataframes to existing sql tables.
    This also serves as a wrapper for basic functionality such as creating new tables from dataframes,
    removing tables, updating table schemas, and listing tables/schemas.
    Currently works with mysql and postgres databases.
</h4>

<h4>Installation / Dependencies</h4>
<p>Dependencies: sqlalchemy, pymysql, pg8000</p>

```bash

pip install pandas-sql-wrapper

```

<h4>Getting Started</h4>
<p>
    Create an instance of PandasSQLWrapper supplying a database connection configuration.
    Either supply a dict or a string path to a json file as shown below.
</p>

```python

sql_data = PandasSQLWrapper({
    host: '<host name>',
    db: '<database name>',
    user: '<database username>',
    password: '<database password>'
})

sql_data = PandasSQLWrapper(configured_from='sql_config.json')

```

<h4>Additional Options</h4>

```python

sql_data = PandasSQLWrapper(
    configured_from='sql_config.json',
    postgres=False, # set to true if connecting to a postgres database
    verbose=False, # set to true for console logging of sql actions
    echo=False # set to true for sql database to communicate back performed actions
)

```

<h4>Update Table</h4>
<p>
    Performs an upsert on a sql table and updates table schema by adding columns if necessary.
    Additionally, user can specify the option to remove rows and columns as part of the update.
    NOTE: The upsert is implemented differently depending on whether the database is mysql or postgres.
    For mysql, upsert is done using REPLACE INTO. For postgres, upsert is done using INSERT INTO ... ON CONFLICT.
</p>

```python

    sql_data.update_table(
        '<table name>',
        df,
        permit_deletes=False # set to True if it is ok to delete rows or columns from sql table not found in dataframe
    )

```

<h4>Other Helper Functions</h4>

```python

    # Create a new table
    sql_data.to_new_table(
        '<table name>',
        df
    )

    # Remove a table
    sql_data.remove_table(
        '<table name>'
    )

    # Get a table from database as a dataframe
    df = sql_data.get_table(
        '<table name>',
        cols=['*'], # provide an array of column names as strings to select only the ones you want
        limit=<int> # get only the first n rows from table
    )

    # List all tables in database
    sql_data.all_tables()

    # Add / Remove columns from a table
    sql_data.add_column(
        '<table name>',
        '<col name>',
        '<data type>' # must be an acceptable sql data type
    )

    sql_data.remove_column(
        '<table name>',
        '<col name>'
    )

    # Custom SQL query
    sql_data.query(
        '<sql expression or statement>'
    )

```