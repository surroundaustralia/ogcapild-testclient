"""
Minimal OGC API implementation must return for the following endpoints:

/                                                       landing_page
/api                                                    api
/conformance                                            conformance
/collections                                            collections
/collections/{collection-id-1}                          first_collection
/collections/{collection-id-1}/items                    first_collection_features
/collections/{collection-id-1}/items/{feature-id-1}     first_collection_first_feature
"""
from config import *


ENDPOINTS = {
    "landing_page": None,
    "conformance": None,
    "collections": None,
    "first_collection": None,
    "first_collection_features": None,
    "first_collection_first_feature": None,
}


def get_endpoint_status(endpoint_key: str):
    try:
        with urllib.request.urlopen(urllib.request.Request(ENDPOINTS[endpoint_key], method="HEAD")) as response:
            if response.code == 200:
                logging.info("Endpoint Status:\t{}:\tPASS".format(endpoint_key))
                return True
            else:
                logging.info("Endpoint Status:\t{}:\tFAIL".format(endpoint_key))
                return False
    except:
        logging.info("Endpoint Status:\t{}:\tFAIL".format(endpoint_key))
        return False


def get_endpoint_html(endpoint_key: str):
    try:
        with urllib.request.urlopen(ENDPOINTS[endpoint_key]) as response:
            if response.code == 200:
                return response.read()
            else:
                return None
    except:
        logging.info("Endpoint HTML:\t{}:\tFAIL (got None)".format(endpoint_key))
        return None


def get_endpoint_json(endpoint_key: str):
    try:
        with urllib.request.urlopen(urllib.request.Request(ENDPOINTS[endpoint_key], headers=)) as response:
            if response.code == 200:
                return response.read()
            else:
                return None
    except:
        logging.info("Endpoint HTML:\t{}:\tFAIL (got None)".format(endpoint_key))
        return None


def get_endpoint_geojson(endpoint_key: str):
    try:
        with urllib.request.urlopen(ENDPOINTS[endpoint_key]) as response:
            if response.code == 200:
                return response.read()
            else:
                return None
    except:
        logging.info("Endpoint HTML:\t{}:\tFAIL (got None)".format(endpoint_key))
        return None


def validate_html(data):
    if data.startswith("<"):
        return False

    return True


def get_landing_page_status(url: str):
    lp = get_endpoint_status(url, "landing_page")
    if lp:
        # since this has passed, define as many other endpoints as we can
        lp_url = url if url.endswith("/") else url + "/"
        ENDPOINTS["landing_page"] = lp_url
        ENDPOINTS["api"] = lp_url + "api"
        ENDPOINTS["conformance"] = lp_url + "conformance"
        ENDPOINTS["collections"] = lp_url + "collections"

    return lp


def get_api_status():
    if ENDPOINTS["api"] is None:
        raise Exception("You must run get_landing_page_status() before running this test")

    return get_endpoint_status(ENDPOINTS["api"], "api")


def get_conformance_status():
    if ENDPOINTS["conformance"] is None:
        raise Exception("You must run get_landing_page_status() before running this test")

    return get_endpoint_status(ENDPOINTS["conformance"], "conformance")


def get_collections_status():
    if ENDPOINTS["collections"] is None:
        raise Exception("You must run get_landing_page_status() before running this test")

    c = get_endpoint_status(ENDPOINTS["collections"], "collections")

    if c:
        # get the ID of the first collection
        d = get_endpoint_html(ENDPOINTS["collections"])
        r = "Endpoint Content validity:\tcollections:\t{}"
        if validate_html(d):
            logging.info(r.format("PASS"))
        else:
            logging.info(r.format("FAIL"))




    ENDPOINTS["first_collection"] = ENDPOINTS["landing_page"] + collection_id
    return c


def get_first_collection_status(collection_id: str):
    if ENDPOINTS["first_collection"] is None:
        raise Exception("You must run get_collections_status() before running this test")

    return get_endpoint_status(ENDPOINTS["first_collection"], "first_collection")


def get_first_collection_features_status():
    if ENDPOINTS["first_collection_features"] is None:
        raise Exception("You must run get_first_collection_status() before running this test")

    return get_endpoint_status(ENDPOINTS["first_collection_features"], "first_collection_features")


def get_first_collection_first_feature_status():
    if ENDPOINTS["first_collection_first_feature"] is None:
        raise Exception("You must run get_first_collection_features_status() before running this test")

    return get_endpoint_status(ENDPOINTS["first_collection_first_feature"], "first_collection_first_feature")


if __name__ == "__main__":
    start_logger()
    logging.info("running test_endpoints main()")
    get_landing_page_status("https://google.com/ggggg")



