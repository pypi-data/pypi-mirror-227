import sys
import traceback
import typeguard

from .._utils import format_analytics_logs, get_log_flag
from typing import Callable, Any, Dict
from functools import wraps
from ._exceptions import BadRequestException, ApiResponseException, QueryLimitException, ValueErrorException
from .._base import _log_usage

import inspect

typechecked: Callable = typeguard.typechecked


def not_null(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        for arg in args:
            if not arg:
                raise BadRequestException("Null or empty parameter is not allowed.")

        return func(*args, **kwargs)

    return wrapper


def error_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (BadRequestException, ValueErrorException) as e:
            wrappers = [x.name for x in traceback.extract_stack() if x.name == "error_handler"]
            if len(wrappers) > 1:
                raise ValueErrorException(str(e)) from None
            else:
                sys.stderr.write(str(e))
        except ApiResponseException as e:
            if e.status_code == 404:
                sys.stderr.write("Specified data not Found. ")
            else:
                raise ValueErrorException(str(e)) from None
        except QueryLimitException as e:
            # Some exceptions need to be propagated back to the caller as-is
            raise
        except Exception as e:
            raise ValueErrorException(str(e)) from None

    return wrapper


def log_usage(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_passed_in_function = [repr(a) for a in args]
        kwargs_passed_in_function = [f"{k}={v!r}" for k, v in kwargs.items()]
        formatted_arguments = ",".join(args_passed_in_function + kwargs_passed_in_function)

        flag = get_log_flag(func)

        try:
            value = func(*args, **kwargs)
            if flag:
                _log_usage.info(format_analytics_logs(function=func.__name__, params=f"params={formatted_arguments}", component=func.__module__))
            return value
        except:
            if flag:
                _log_usage.error(format_analytics_logs(function=func.__name__, params=f"params={formatted_arguments}", component=func.__module__))
            raise

    return wrapper
