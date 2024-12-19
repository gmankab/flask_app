# ruff: noqa: F401

import api.user as __user__
import api.data as __data__
import app.common
import app.models
import flasgger
import waitress
import asyncio


if __name__ == '__main__':
    swagger = flasgger.Swagger(app.common.app)
    asyncio.run(app.common.init_models())
    waitress.serve(app.common.app, listen='*:8080')

