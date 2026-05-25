import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class ParquetService:
    def __init__(self, service_name="Clerk Platform"):
        self.service_name = service_name

    def generate_kpi_data(self, days=30, records_per_hour=1):
        """"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        timestamps = pd.date_range(
            start=start_time,
            end=end_time,
            freq=f'{60//records_per_hour}min'
        )

        data = []

        for timestamp in timestamps:
            traffic_multiplier = 1.0

            record = {
                'timestamp': timestamp,
                'date': timestamp.date(),
                'hour': timestamp.hour,
                'service_name': self.service_name,
                'requests_per_minute': max(0, int(np.random.normal(
                    100 * traffic_multiplier, 20
                ))),
                'unique_users': max(0, int(np.random.normal(
                    50 * traffic_multiplier, 10
                ))),
            }

            data.append(record)
        return pd.DataFrame(data)
        
    def write_file(self, file_path, df: pd.DataFrame):
        df.to_parquet(file_path, engine="pyarrow", index=False)

    def read_file(eslf, file_path):
        df = pd.read_parquet(file_path, engine="pyarrow")
        return df