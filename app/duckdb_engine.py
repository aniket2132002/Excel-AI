import duckdb

class DuckDBEngine:
    def __init__(self):
        self.conn = duckdb.connect(database=":memory:")

    def register_tables(self, dataframes: dict):
        """
        Register valid Pandas DataFrames as DuckDB tables.
        """
        for table_name, df in dataframes.items():
            # 🔒 Safety checks
            if df is None:
                continue
            if df.shape[1] == 0:
                continue
            if df.shape[0] == 0:
                continue

            self.conn.register(table_name, df)

    def execute(self, sql: str):
        """
        Execute SQL and return Pandas DataFrame.
        """
        return self.conn.execute(sql).fetchdf()
