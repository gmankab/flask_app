from pathlib import Path

db_url: str = 'sqlite+aiosqlite:///:memory:'
app_path = Path(__file__).parent.parent.resolve()
tests_path = app_path / 'tests'

