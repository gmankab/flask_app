# ruff: noqa: F401

import app.common
import app.models
import api.user as __user__
import api.data as __data__
import asyncio


if __name__ == '__main__':
    asyncio.run(app.common.init_models())
    app.common.app.run()

