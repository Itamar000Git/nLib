from functools import wraps
import logging

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info(f"Calling function '{func.__name__}' with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Function '{func.__name__}' returned {result}")
            return result
        except Exception as e:
            logging.error(f"Exception in function '{func.__name__}': {e}")
            raise e
    return wrapper