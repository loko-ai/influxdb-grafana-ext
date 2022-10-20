# using Sanic
import json
import traceback

import sanic
from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound
from sanic_openapi import swagger_blueprint

from loko_extensions.business.decorators import extract_value_args
from utils.logger_utils import stream_logger

logger = stream_logger(__name__)

def get_app(name):
    app = Sanic(name)
    swagger_blueprint.url_prefix = "/api"
    app.blueprint(swagger_blueprint)
    return app


name = "first_project"
app = get_app(name)
bp = Blueprint("default", url_prefix=f"/")
app.config["API_TITLE"] = name

@bp.post('/myfirstservice')
@extract_value_args()
async def f(value, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {value}')
    n = int(args.get('n'))
    return sanic.json(dict(msg=f"{'#'*n} Hello world! {'#'*n}"))

@bp.post('/upload_file')
@extract_value_args(file=True)
async def f2(file, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {file[0].name}')
    n = int(args.get('n'))
    return sanic.json(dict(msg=f"{'#'*n} You have uploaded the file: {file[0].name}! {'#'*n}"))

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
