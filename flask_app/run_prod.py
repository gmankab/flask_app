# ruff: noqa: F401

import app.common
import app.models
import api.user as __user__
import api.data as __data__
import asyncio
import waitress


if __name__ == '__main__':
    asyncio.run(app.common.init_models())
    waitress.serve(app.common.app, listen='*:8080')

