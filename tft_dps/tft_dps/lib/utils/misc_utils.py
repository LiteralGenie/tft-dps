# https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module


from itertools import islice
from pathlib import Path
from typing import Generator


def log_http_requests():
    import logging
    from http.client import HTTPConnection

    """Switches on logging of the requests module."""
    HTTPConnection.debuglevel = 2

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True


def to_path(x: str | Path):
    fp = x
    if isinstance(fp, str):
        fp = Path(fp)
    return fp


# https://docs.python.org/3/library/itertools.html#itertools.batched
def batched(iterable, n, *, strict=False) -> "Generator[tuple]":
    # batched('ABCDEFG', 2) → AB CD EF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch
