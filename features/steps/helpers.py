from typing import Type


def capture_exception(exception_type: Type[Exception]):
    def decorator(func):
        def wrapper(context, *args, **kwargs):
            try:
                return func(context, *args, **kwargs)
            except exception_type as error:
                context.last_error = error

        return wrapper

    return decorator
