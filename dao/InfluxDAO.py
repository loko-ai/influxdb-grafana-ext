import json
from datetime import datetime
from typing import List

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from utils.logger_utils import logger


class InfluxDAO:
    def __init__(self, url='http://influxdb-grafana-ext_influxdb:8086', org='influx-org', username='influx-user',
                 password='influx-pass', bucket='influx-bu'):
        logger.debug(f"INFLUXDB URL:: {url}")
        self.client = InfluxDBClient(url=url, org=org, username=username, password=password)
        self.bucket = bucket

    def save(self, records: List[dict], measurement: str, tags: list, fields: list, time: str = None):

        def get_record(row):
            _tags = {k: row[k] for k in tags}
            _fields = {k: row[k] for k in fields}
            record = dict(measurement=measurement, tags=_tags, fields=_fields)
            if time:
                record['time'] = row[time]
            return record

        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        _records = [get_record(row) for row in records]
        logger.debug(f"Bucket:: {self.bucket}, measurement:: {measurement}")
        write_api.write(bucket=self.bucket, record=_records)

    def delete(self, measurement: str, start=None, stop=None):

        delete_api = self.client.delete_api()

        start = start or "1970-01-01T00:00:00Z"
        stop = stop or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        delete_api.delete(start, stop, predicate=f'_measurement="{measurement}"', bucket=self.bucket)

    def query(self, start='-50m'):

        query_api = self.client.query_api()
        start = start or '-50m'
        tables = query_api.query(f'from(bucket:"{self.bucket}") |> range(start: {start})')

        return json.loads(tables.to_json())


if __name__ == '__main__':
    import csv

    # data_path = "/home/roberta/old_pc/terna_lib/dati/v3_bis/fake_data.csv"

    data_path = '/home/cecilia/Scaricati/fake_data.csv'
    influxdao = InfluxDAO(url='http://localhost:8086')

    measurement = 'fake_data'

    influxdao.delete(measurement)

    print(influxdao.query())

    with open(data_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        cols = next(csv_reader)
        records = [dict(zip(cols, row)) for row in csv_reader]
        # print(records)
        influxdao.save(records, measurement, tags=['Linea', 'Traliccio'], fields=['orario'])

    print(influxdao.query())


