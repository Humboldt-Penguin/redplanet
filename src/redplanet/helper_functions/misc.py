from contextlib import contextmanager
import time

@contextmanager
def timer(message=''):
    start = time.time()
    yield
    end = time.time()
    print(f'{message}{end - start:.3f} seconds')
