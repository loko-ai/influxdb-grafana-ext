import json
from datetime import datetime
from typing import List

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from utils.logger_utils import logger


class InfluxDAO:
    def __init__(self, url='http://influxdb-grafana-ext_influxdb:8086', org='influx-org', username='influx-user',
                 password='influx-pass'):
        logger.debug(f"INFLUXDB URL:: {url}")
        self.client = InfluxDBClient(url=url, org=org, username=username, password=password, timeout=172800)

    def save(self, records: List[dict], measurement: str = None, tags: list = None, fields: list = None, time: str = None,
             bucket='influx-bu'):

        options = SYNCHRONOUS
        tags = tags or []

        def get_record(row):
            _tags = {k: row[k] for k in tags}
            _fields = {k: row[k] for k in fields}
            record = dict(measurement=measurement, tags=_tags, fields=_fields)
            if time:
                record['time'] = row[time]
            return record

        write_api = self.client.write_api(write_options=options)
        _records = [get_record(row) for row in records] if measurement else records
        logger.debug(f"Bucket:: {bucket}, measurement:: {measurement}")
        write_api.write(bucket=bucket, record=_records)

    def delete(self, measurement: str = None, predicate: str = None, start=None, stop=None, bucket='influx-bu'):

        if measurement:
            predicate = f'_measurement="{measurement}"'

        delete_api = self.client.delete_api()

        start = start or "1970-01-01T00:00:00Z"
        stop = stop or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        delete_api.delete(start, stop, predicate=predicate, bucket=bucket)

    def read(self, measurement: str, start=None, stop=None, bucket='influx-bu'):
        query_api = self.client.query_api()
        start = start or "1970-01-01T00:00:00Z"
        stop = stop or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        tables = query_api.query(f'from(bucket:"{bucket}") |> range(start: {start}, stop: {stop}) '
                                 f'|> filter(fn: (r) => r._measurement == "{measurement}")')

        return json.loads(tables.to_json())

    def query(self, query: str):

        query_api = self.client.query_api()
        tables = query_api.query(query)

        return json.loads(tables.to_json())


if __name__ == '__main__':
    import csv

    # data_path = "/home/roberta/old_pc/terna_lib/dati/v3_bis/fake_data.csv"

    data_path = '/home/cecilia/Scaricati/fake_data.csv'
    influxdao = InfluxDAO(url='http://localhost:8086')

    measurement = 'fake_data'

    # influxdao.delete(measurement)

    print(influxdao.read(start='2021-05-22T23:30:00Z'))

    # with open(data_path) as f:
    #     csv_reader = csv.reader(f, delimiter=',')
    #     cols = next(csv_reader)
    #     records = [dict(zip(cols, row)) for row in csv_reader]*10000
    #     # print(records)
    #     influxdao.save(records, measurement, tags=['Linea', 'Traliccio'], fields=['valore'], asynchronous=False)
    #     print('SAVED')
    #
    # print(influxdao.read())


