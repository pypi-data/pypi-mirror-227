from functools import lru_cache

import httpx


@lru_cache
def fibonacci(num: int) -> int:
    """
    Returns fibonacci number based on provided integer
    """
    if num in (0, 1):
        return num

    return fibonacci(num - 1) + fibonacci(num - 2)


@lru_cache
def tribonacci(num: int) -> int:
    """
    Returns tribonacci number based on provided integer
    """
    if num in (0, 1):
        return 0

    if num == 2:
        return 1

    return tribonacci(num - 1) + tribonacci(num - 2) + tribonacci(num - 3)


def get_url(url: str, https: bool = False):
    if not url.startswith("http"):
        url = f"http{'s' if https else ''}://{url}"

    return httpx.get(url)


async def aget_url(url: str, https: bool = False):
    if not url.startswith("http"):
        url = f"http{'s' if https else ''}://{url}"

    client = httpx.AsyncClient()
    return await client.get(url)
