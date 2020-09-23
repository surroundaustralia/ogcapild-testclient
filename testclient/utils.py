from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from enum import Enum
import json


class MediaType(Enum):
    HTML = "text/html"
    JSON = "application/json"
    GEOJSON = "application/geo+json"
    TURTLE = "text/turtle"


def get_http_status(url: str):
    try:
        r = urlopen(Request(url, method="HEAD"))
    except HTTPError as e:
        return e.code
    except URLError as e:
        return e.reason
    else:
        return r.getcode()


def get_url_content(url: str, media_type: MediaType = None):
    if media_type is None:
        media_type = MediaType.HTML
    try:
        with urlopen(Request(url, headers={"Accept": str(media_type.value)})) as response:
            if response.code == 200:
                if media_type == MediaType.JSON or media_type == MediaType.GEOJSON:
                    return 200, json.loads(response.read())
                else:
                    return 200, response.read().decode()
            else:
                return response.code, None
    except:
        return response.code, None


def is_url_ok(url: str, media_type: MediaType = None):
    if media_type is None:
        media_type = MediaType.HTML
    try:
        with urlopen(Request(url, headers={"Accept": str(media_type.value)})) as response:
            if response.code >= 200 and response.code <= 300:
                return True
            else:
                return False
    except:
        return False
