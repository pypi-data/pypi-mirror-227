import time
import datetime
from typing import Dict, List
from urllib.parse import parse_qs, urlparse

__all__ = ["Helper"]


class Helper(object):
    """
    A helper class
    """

    @staticmethod
    def get_current_time() -> str:
        """
        Get the current time string with given format.
        :return: the formatted time string
        """
        current_ts = datetime.datetime.now()
        current_ts_str = current_ts.strftime("%Y%m%d%H%M%S")
        return current_ts_str

    @staticmethod
    def get_url_params(url: str) -> Dict[str, list[str]]:
        """
        Get the parameters of a request
        :param url: the request
        :return: dictionary of parameters
        """
        return parse_qs(urlparse(url).query)
