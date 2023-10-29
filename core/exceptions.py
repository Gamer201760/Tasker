class TaskerException(Exception):
    ...

class UnAuthorized(TaskerException):
    """Не получилось авторизоваться"""
    def __init__(self, *args: object) -> None:
        super().__init__('Неверное имя пользователя или пароль')


class AlreadyExist(TaskerException):
    """Объект уже существует"""
    def __init__(self, *args: object) -> None:
        super().__init__('Объект уже существует')
