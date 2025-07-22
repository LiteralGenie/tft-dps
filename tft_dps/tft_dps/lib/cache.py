import functools
import json
from pathlib import Path
from typing import Callable


class Cache:
    def has(self, key: str) -> bool:
        raise NotImplementedError()

    def get(self, key: str) -> str:
        raise NotImplementedError()

    def set(self, key: str, value: str) -> None:
        raise NotImplementedError()


class NativeFileCache(Cache):
    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_fp(self, key: str):
        return self.cache_dir / key

    def has(self, key: str) -> bool:
        return self._get_fp(key).exists()

    def get(self, key: str) -> str:
        return self._get_fp(key).read_text()

    def set(self, key: str, value: str) -> None:
        self._get_fp(key).write_text(value)


def fetch_cached(
    fetch_fn: Callable,
    cache: Cache,
    key: str,
) -> str:
    if not cache.has(key):
        print("Fetching", key)
        resp = fetch_fn()
        cache.set(key, resp)

    return cache.get(key)


@functools.wraps(fetch_cached)
def fetch_cached_json(*args, **kwargs) -> dict:
    return json.loads(fetch_cached(*args, **kwargs))
