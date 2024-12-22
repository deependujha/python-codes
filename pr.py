from contextlib import contextmanager

@contextmanager
def my_ctx(*args, **kwargs):
    try:
        print('Entering context')
        yield 'hello'
    except Exception as e:
        print(f'Caught exception: {e}')
    finally:
        print('Exiting context')

if __name__ == '__main__':
    with my_ctx() as val:
        print(f'Value: {val}')
    print("-"*50)