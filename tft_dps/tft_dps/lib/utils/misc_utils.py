# https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module


from pathlib import Path


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
