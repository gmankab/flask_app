### run locally

by default in-memory database is used, you may want set path for database in `flask_app/app/config.py` file, after that you can run code

```shell
python -m ensurepip
python -m pip install uv
python -m uv venv
python -m uv pip install -r pyproject.toml --python=.venv/bin/python
.venv/bin/python flask_app/run_dev.py
```
run_dev.py - run app on local machine for development and debugging with `flask run`

run_prod.py - run app for production with `waitress`

### api testing with curl


```shell
curl -X POST http://localhost:5000/user/create -H "Content-Type: application/json" \
-d '{"username": "user1", "email": "user1@example.com"}'
```

```shell
curl -X GET "http://localhost:5000/user/get?id=1"
```

```shell
curl -X POST http://localhost:5000/user/update -H "Content-Type: application/json" \
-d '{"id": 1, "username": "user1_new", "email": "user1_new@example.com"}'
```

```shell
curl -X GET http://localhost:5000/user/list-all
```

```shell
curl -X POST http://localhost:5000/user/delete -H "Content-Type: application/json" -d '{"id": 1}'
```

### linting

`ruff` and `pyright` linters are used


```shell
python -m uv pip isntall ruff pyright
.venv/bin/ruff check flask_app
.venv/bin/pyright flask_app
```

