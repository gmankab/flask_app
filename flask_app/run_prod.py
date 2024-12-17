import app.common
import app.models
import app.api
import asyncio
import waitress


if __name__ == '__main__':
    asyncio.run(app.common.init_models())
    waitress.serve(app.common.app, listen='*:8080')

