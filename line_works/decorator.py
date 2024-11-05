import json
from os import makedirs
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

from line_works import config

if TYPE_CHECKING:
    from line_works import LineWorks

T = TypeVar("T")
P = ParamSpec("P")


def save_cookie(func: Callable[P, T]) -> Callable[P, T]:
    """save session with json file

    Args:
        func (Callable): function

    Returns:
        Callable: wrapper function
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        result = func(*args, **kwargs)

        m: LineWorks = args[0]  # type: ignore

        makedirs(config.SESSION_DIR, exist_ok=True)
        with open(m.cookie_path, "w") as json_file:
            json.dump(m.session.cookies.get_dict(), json_file, indent=4)  # type: ignore

        return result

    return wrapper
