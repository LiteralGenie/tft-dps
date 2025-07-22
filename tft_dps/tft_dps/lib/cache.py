import functools
import json
from pathlib import Path
from typing import Callable


class Cache:
    async def has(self, key: str) -> bool:
        raise NotImplementedError()

    async def get(self, key: str) -> str:
        raise NotImplementedError()

    async def set(self, key: str, value: str) -> None:
        raise NotImplementedError()


class NativeFileCache(Cache):
    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_fp(self, key: str):
        return self.cache_dir / key

    async def has(self, key: str) -> bool:
        return self._get_fp(key).exists()

    async def get(self, key: str) -> str:
        return self._get_fp(key).read_text()

    async def set(self, key: str, value: str) -> None:
        self._get_fp(key).write_text(value)


async def fetch_cached(
    fetch_fn: Callable,
    cache: Cache,
    key: str,
) -> str:
    if not await cache.has(key):
        print("Fetching", key)
        resp = await fetch_fn()
        await cache.set(key, resp)

    return await cache.get(key)


@functools.wraps(fetch_cached)
async def fetch_cached_json(*args, **kwargs) -> dict:
    return json.loads(await fetch_cached(*args, **kwargs))
