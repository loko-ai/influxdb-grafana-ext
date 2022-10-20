import concurrent

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.write_api import ASYNCHRONOUS

import asyncio


import sys

from influxdb_client import InfluxDBClient, Point
from influxdb_client .client.write_api import SYNCHRONOUS
import csv

data_path = "/home/roberta/old_pc/terna_lib/dati/v3_bis/fake_data.csv"

# token = "zUVl5l0kAsGNVY7uMcfm9ej61n8sLVHuJYy5sdwiz_nuD2yJJAO-xvKbPTITFDRiWstzGmneXghNuuRGOIc0NA=="
bucket = "influx-bu"




def prepare_data(measurement_name, data_path):
    records = []
    with open(data_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        cols = next(csv_reader)
        for row in csv_reader:
            row_dict = dict(zip(cols, row))
            tags = dict(linea=row_dict['Linea'], traliccio=row_dict['Traliccio'])
            fields = dict(orario_picco=row_dict['orario picco'], altro=3)
            records.append(
                dict(measurement=measurement_name, tags=tags, fields=fields, time='2022-10-20T14:44:16.952426+00:00'))


async def main(executor, data_path):
    loop = asyncio.get_running_loop()
    async with InfluxDBClientAsync(
        url="http://localhost:8086", org="influx-org", username='influx-user',
                        password='influx-pass') as client:
        # write_api = client.write_api(write_options=SYNCHRONOUS)


        measurement_name = 'h2o_feet'

        records = await loop.run_in_executor(executor, prepare_data, measurement_name, data_path)


        # write_api.write(bucket=bucket, record=records)


        # tables = client.query_api().query('from(bucket:"influx-bu") |> range(start: -50m)')

        # Serialize to JSON
        # output = tables.to_json(indent=5)
        # print(output)
        await client.write_api().write(bucket=bucket, record=records)
    return "done"


executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
if __name__ == "__main__":
    a = asyncio.run(main(executor, data_path))
    print(a)


# client = InfluxDBClient(url="http://localhost:8086", org="influx-org", username='influx-user',
#                         password='influx-pass')

#
#
# delete_api = client.delete_api()
#
# """
# Delete Data
# """
# start = "1970-01-01T00:00:00Z"
# stop = "2023-02-01T00:00:00Z"
# delete_api.delete(start, stop, '_measurement="h2o_feet"', bucket=bucket)

#
# write_api = client.write_api(write_options=SYNCHRONOUS)
#
#
# measurement_name = 'h2o_feet'
# records = []
#
# with open(data_path) as f:
#     csv_reader = csv.reader(f, delimiter=',')
#     cols = next(csv_reader)
#     for row in csv_reader:
#         row_dict = dict(zip(cols,row))
#         tags = dict(linea=row_dict['Linea'], traliccio=row_dict['Traliccio'])
#         fields = dict(orario_picco=row_dict['orario picco'], altro=3)
#         records.append(dict(measurement=measurement_name, tags=tags, fields=fields, time='2022-10-20T14:44:16.952426+00:00'))
#
#
#
# write_api.write(bucket=bucket, record=records)
#
#
# tables = client.query_api().query('from(bucket:"influx-bu") |> range(start: -50m)')
#
# # Serialize to JSON
# output = tables.to_json(indent=5)
# print(output)


