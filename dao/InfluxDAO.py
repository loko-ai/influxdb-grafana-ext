from datetime import datetime
from typing import List

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDAO:
    def __init__(self, url='http://localhost:8086', org='influx-org', username='influx-user',
                 password='influx-pass', bucket='influx-bu'):
        self.client = InfluxDBClient(url=url, org=org, username=username, password=password)
        self.bucket = bucket

    def save(self, records: List[dict], measurement: str, tags: list, fields: list, time: str = None):

        def get_record(row):
            _tags = {k: row[k] for k in tags}
            _fields = {k: row[k] for k in fields}
            record = dict(measurement=measurement, tags=_tags, fields=_fields)
            if time:
                record['time'] = row['time']
            return record

        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        _records = [get_record(row) for row in records]
        write_api.write(bucket=self.bucket, record=_records)

    def delete(self, measurement: str, start="1970-01-01T00:00:00Z", stop=None):

        delete_api = self.client.delete_api()

        stop = stop or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        delete_api.delete(start, stop, predicate=f'_measurement="{measurement}"', bucket=self.bucket)

    def query(self, start='-50m'):

        query_api = self.client.query_api()

        tables = query_api.query(f'from(bucket:"{self.bucket}") |> range(start: {start})')

        return tables.to_json(indent=5)


if __name__ == '__main__':
    import csv

    data_path = '/home/cecilia/Scaricati/fake_data.csv'
    influxdao = InfluxDAO()

    measurement = 'fake_data'

    influxdao.delete(measurement)

    print(influxdao.query())

    with open(data_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        cols = next(csv_reader)
        records = [dict(zip(cols, row)) for row in csv_reader]
        influxdao.save(records, measurement, tags=['Linea', 'Traliccio'], fields=['orario picco'])

    print(influxdao.query())


