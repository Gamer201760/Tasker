class TaskerException(Exception):
    ...

class UnAuthorized(TaskerException):
    "Не получилось авторизоваться"


class AlreadyExist(TaskerException):
    "Объект уже существует"
