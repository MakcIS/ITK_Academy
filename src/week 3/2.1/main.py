import asyncio


def async_retry(retries: int = 0, exceptions: None | tuple = None):
    if exceptions is None:
        exceptions = Exception

    def decorator(func):
        async def wrapper(*args, **kwargs):
            counter = 0
            while True:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except exceptions as err:
                    if counter >= retries:
                        raise err

                    counter += 1
                    print(f"Retrying unstable_task ({counter}/{retries})...")
                    continue

        return wrapper

    return decorator


@async_retry(retries=3, exceptions=(ValueError,))
async def unstable_task():
    print("Running task...")
    raise ValueError("Something went wrong")


async def main():
    try:
        await unstable_task()
    except Exception as e:
        print(f"Final failure: {e}")


asyncio.run(main())
