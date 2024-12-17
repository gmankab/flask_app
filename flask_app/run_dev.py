import app.common
import app.models
import app.api
import asyncio


if __name__ == '__main__':
    asyncio.run(app.common.init_models())
    app.common.app.run()

