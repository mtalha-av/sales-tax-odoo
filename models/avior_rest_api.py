import logging

_logger = logging.getLogger(__name__)


class AviorRESTService:
    def __init__(self, username, password, url, timeout=300, enable_log=False):
        self.username = username
        self.password = password
        self.url = url
        self.timeout = timeout
        self.enable_log = enable_log
