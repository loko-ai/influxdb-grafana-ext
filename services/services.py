import traceback

import sanic
from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound, SanicException
from sanic_openapi import swagger_blueprint

from loko_extensions.business.decorators import extract_value_args

from dao.InfluxDAO import InfluxDAO
from utils.logger_utils import logger


def get_app(name):
    app = Sanic(name)
    swagger_blueprint.url_prefix = "/api"
    app.blueprint(swagger_blueprint)
    return app


name = "first_project"
app = get_app(name)
bp = Blueprint("default", url_prefix=f"/")
app.config["API_TITLE"] = name
app.config["REQUEST_MAX_SIZE"] = 20000000000
app.config["REQUEST_TIMEOUT"] = 172800


influxdao = InfluxDAO()

@bp.post('/save_data')
@extract_value_args()
async def save_data(value, args):
    logger.debug(f'ARGS: {args}')

    bucket = args.get('bucket_save')

    manual = args.get('manual')

    if manual:

        measurement_name = args.get("measurement_name", None)
        if not measurement_name:
            raise SanicException("Measurement name not specified", status_code=400)

        fields_keys = args.get("fields", [])
        if len(fields_keys)==0:
            raise SanicException("Fields values needs to be specified", status_code=400)
        fields_keys = [fields_keys[i]["field_key"] for i in range(len(fields_keys))]

        tags_keys = args.get("tags", [])
        if len(fields_keys) == 0:
            raise SanicException("Tags values needs to be specified", status_code=400)
        tags_keys = [tags_keys[i]["tag_key"] for i in range(len(tags_keys))]

        time_key = args.get("time", None)

        influxdao.save(bucket=bucket, records=value, measurement=measurement_name, tags=tags_keys,
                       fields=fields_keys, time=time_key)

    else:

        influxdao.save(bucket=bucket, records=value)


    return sanic.json(f"Data correctly saved")

@bp.post('/delete_data')
@extract_value_args()
async def delete_data(value, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {value}')

    bucket = args.get('bucket_del')

    measurement_name = args.get("measurement_delete", None)
    # if not measurement_name:
    #     raise SanicException("Measurement name not specified", status_code=400)
    start = args.get("start_delete", None)
    stop = args.get("stop_delete", None)
    influxdao.delete(bucket=bucket, measurement=measurement_name, predicate=value, start=start, stop=stop)
    return sanic.json(f"Deleted data")

@bp.post('/read')
@extract_value_args()
async def read_data(value, args):
    logger.debug(f'ARGS: {args}')

    bucket = args.get('bucket_read')
    measurement = args.get('measurement_read')

    start = args.get("start_read", None)
    stop = args.get("stop_read", None)
    res = influxdao.read(measurement=measurement, bucket=bucket, start=start, stop=stop)
    return sanic.json(res)

@bp.post('/query')
@extract_value_args()
async def query_data(value, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {value}')

    res = influxdao.query(query=value)
    logger.debug(f"len::: {len(res)}")
    return sanic.json(res)

@app.exception(Exception)
async def manage_exception(request, exception):
    e = dict(error=str(exception))
    if isinstance(exception, NotFound):
        return sanic.json(e, status=404)
    logger.error('TracebackERROR: \n' + traceback.format_exc() + '\n\n')
    status_code = exception.status_code or 500
    return sanic.json(e, status=status_code)


app.blueprint(bp)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
