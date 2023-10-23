import time
from functools import wraps

def retry(max_retries=3, retry_delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = max_retries
            while retries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries -= 1
                    if retries == 0:
                        print(f"Max retries reached for function {func.__name__}.")
                        raise
                    else:
                        print(f"Error in function {func.__name__}: {str(e)}")
                        print(f"Retrying function {func.__name__} in {retry_delay} seconds...")
                        time.sleep(retry_delay)
        return wrapper
    return decorator