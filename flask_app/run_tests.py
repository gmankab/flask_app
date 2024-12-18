# ruff: noqa: F401

import app.config
import app.models
import api.user as __user__
import api.data as __data__
import pytest
import sys


if __name__ == "__main__":
    print(app.config.tests_path)
    to_test: list[str] = []
    for file in app.config.tests_path.iterdir():
        to_test.append(str(file))
    exit_code = pytest.main(to_test)
    sys.exit(exit_code)

