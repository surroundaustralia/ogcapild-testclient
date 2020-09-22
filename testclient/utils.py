from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from enum import Enum
import json


class SupportedMediaType(Enum):
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


def get_content_by_accept(url: str, media_type: SupportedMediaType):
    try:
        with urlopen(Request(url, headers={"Accept": str(media_type)})) as response:
            print(response.)
            if response.code == 200:
                if media_type == SupportedMediaType.JSON or media_type == SupportedMediaType.GEOJSON:
                    return json.loads(response.read())
                else:
                    return response.read().decode()
            else:
                return None
    except:
        return None
