import json
import datetime
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy.sql import text


class PandasSQLWrapper(object):

    def __init__(self, configured_from, verbose=False, echo=False):
        self.host, self.db, self.user, self.password = self.configure(configured_from)
        self.verbose = verbose
        self.con = self.establish_connection(echo=echo)

    def query(self, statement):
        return pd.read_sql_query(statement, self.con)

    def all_tables(self):
        return self.query("SHOW tables")

    def get_table(self, table_name, cols=["*"], limit=1000000):
        cols = ", ".join(cols)
        return self.query("SELECT {} FROM {} LIMIT {}".format(
            cols, table_name, "0, {}".format(limit)
        ))

    def to_new_table(self, table_name, df):
        if self.verbose:
            print("Creating new table {}.".format(table_name))
        df.to_sql(table_name, self.con, if_exists='fail')

    def list_features(self, table_name):
        return self.query("SHOW COLUMNS FROM {}".format(table_name)).Field.values

    def remove_table(self, table_name):
        assert table_name in self.all_tables().values.ravel(), "Table with name `{}` does not exist to be removed."\
            .format(table_name)
        if self.verbose:
            print("Removing table {}.".format(table_name))
        self.con.execute("DROP TABLE {}".format(table_name))

    def add_column(self, table_name, col_name, dtype):
        assert col_name not in self.list_features(table_name), "Column: {} already exists in {}"\
            .format(col_name, table_name)
        if self.verbose:
            print("Adding column {} to table {}.".format(col_name, table_name))
        self.con.execute("ALTER TABLE {} ADD COLUMN {} {};".format(table_name, col_name, dtype))

    def remove_column(self, table_name, col_name):
        assert col_name in self.list_features(table_name), "Column: {} not found in {} to be removed"\
            .format(col_name, table_name)
        if self.verbose:
            print("Removing column {} from table {}.".format(col_name, table_name))
        self.con.execute("ALTER TABLE {} DROP COLUMN {};".format(table_name, col_name))

    def database_schema(self):
        return [self.list_features(table_name) for table_name in self.all_tables().Tables_in_yelp_db.values]

    def update_table(self, table_name, df, permit_deletes=False):
        self._update_populate_table(table_name, df)
        if permit_deletes:
            self._update_prune_table(table_name, df)

    def _update_populate_table(self, table_name, df):
        cols = self._sql_string(df.columns)
        symbols = self._sql_string(list(map(lambda col: ":" + str(col), df.columns)))
        self._update_add_columns(table_name, df)
        if self.verbose:
            print("Repopulating table {} rows.".format(table_name))
        self.con.execute(
            text(
                """
                REPLACE INTO {} {} VALUES {}
                """.format(table_name, cols, symbols)
            ),
            self._parameterize_for_sql(df)
        )

    def _update_prune_table(self, table_name, df):
        self._update_drop_columns(table_name, df)
        wanted_rows = self._sql_string(df['id'].values)
        if self.verbose:
            print("Pruning {} of unwanted rows.".format(table_name))
        self.con.execute(
            text(
                """
                DELETE FROM {}
                WHERE id NOT IN {}
                """.format(table_name, wanted_rows)
            )
        )

    def _update_add_columns(self, table_name, df):
        any_new_columns = set(df.columns) - set(self.list_features(table_name))
        if len(any_new_columns) > 0:
            for feature in any_new_columns:
                self.add_column(table_name, feature, self._get_sql_type(df, feature))

    def _update_drop_columns(self, table_name, df):
        unwanted_columns = set(self.list_features(table_name)) - set(df.columns)
        if len(unwanted_columns) > 0:
            for feature in unwanted_columns:
                self.remove_column(table_name, feature)

    def _sql_string(self, cols):
        return "(" + ", ".join(map(str, cols)) + ")"

    def _parameterize_for_sql(self, df):
        cols = df.select_dtypes(include=np.datetime64).columns.values
        records = df.to_dict('records')
        for row in records:
            for col in cols:
                row[col] = str(row[col])
        return records

    def _get_sql_type(self, df, col_name):
        if col_name in df.select_dtypes(include=[int]):
            return 'INTEGER'
        elif col_name in df.select_dtypes(include=[np.datetime64]):
            return 'DATETIME'
        elif col_name in df.select_dtypes(include=[float]):
            return 'FLOAT'
        elif col_name in df.select_dtypes(include=[bool]):
            return 'BOOLEAN'
        elif col_name in df.select_dtypes(include=[object]):
            return 'TEXT'
        else:
            assert False, "Cannot resolve mysql datatype from dataframe column, `{}`. " \
                          "Use the add_column method to expand table schema manually."\
                .format(col_name)

    def establish_connection(self, echo=False):
        con = sqlalchemy.create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(self.user, self.password, self.host, self.db),
            echo=echo
        )
        con.connect()
        return con

    def configure(self, config):
        if isinstance(config, str):
            with open(config) as file:
                config = json.load(file)
        return (config['host'], config['db'], config['user'], config['password'])
