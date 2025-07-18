# https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module
def log_http_requests():
    import contextlib
    import logging
    from http.client import HTTPConnection

    """Switches on logging of the requests module."""
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True
