from pathlib import Path

work_path = Path.home().joinpath('Tasker')
work_path.mkdir(exist_ok=True)

db_path = work_path.joinpath('tasker.db')
