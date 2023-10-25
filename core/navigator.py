from typing import Callable, TypeAlias, TypedDict

page: TypeAlias = tuple[int, Callable | None]


class Pages(TypedDict):
    main: page
    login: page
    calendar: page
