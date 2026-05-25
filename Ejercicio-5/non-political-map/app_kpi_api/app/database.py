import os
import duckdb

class DuckDBManager:
    def __init__(self):
        self.con = None
        self._total_records = 0

    def connect(self):
        """Initialization the singleton connection."""
        self.con = duckdb.connect(database=":memory:")

        self.con.execute("INSTALL httpfs; LOAD httpfs;")

        self.con.execute(f"""
            CREATE SECRET (
                         TYPE S3,
                         PROVIDER config,
                         KEY_ID '{os.getenv('AWS_ACCESS_KEY_ID')}',
                         SECRET '{os.getenv('AWS_SECRET_ACCESS_KEY')}',
                         REGION '{os.getenv('AWS_REGION')}'
            );
        """)

    def disconnect(self):
        """Disposes of the connection and flushes buffers"""
        if self.con:
            self.con.close()
            print("DuckDB connection safely disposed.")

    def get_cursor(self):
        return self.con.cursor()

    def metadata(self):
        """Caches the total count to avoid S3 roundtrips on every page."""
        cursor = self.get_cursor()
        path = os.getenv('S3_DATA_PATH')
        res = cursor.execute(
            f"SELECT COUNT(*) FROM read_parquet('{path}')").fetchone()
        self._total_records = res[0]


db_manager = DuckDBManager()
