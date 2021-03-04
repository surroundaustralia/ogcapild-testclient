import sys
from bs4 import BeautifulSoup

sys.path.append("..")
from testclient.utils import *


def valid_link_object(link: dict) -> tuple:
    valid = True
    messages = []
    if link.get("href") is None:
        valid = False
        messages.append("Link does not have an href attribute")
    else:
        if type(link.get("href")) != str:
            valid = False
            messages.append("The mandatory link href value is not type of string (str)")
        if link.get("rel"):
            if type(link.get("rel")) != str:
                valid = False
                messages.append("Link rel property value is present, but is not type of string (str)")
        if link.get("type"):
            if type(link.get("type")) != str:
                valid = False
                messages.append("Link type property value is present, but is not type of string (str)")
        if link.get("hreflang"):
            if type(link.get("hreflang")) != str:
                valid = False
                messages.append("Link hreflang property value is present, but is not type of string (str)")
        if link.get("title"):
            if type(link.get("title")) != str:
                valid = False
                messages.append("Link title property value is present, but is not type of string (str)")
        if link.get("length"):
            if type(link.get("length")) != int:
                valid = False
                messages.append("Link length property value is present, but is not type of integer")

    return valid, messages


class RequirementTests:
    @staticmethod
    def req_01_test(api_base_url: str):
        messages = []
        result = True

        if not is_url_ok(api_base_url):
            messages.append("API landing page URI, {}, does not respond to a GET request".format(api_base_url))
            result = False
        return result, messages

    @staticmethod
    def req_02_test(api_base_url: str):
        A = True
        B = True
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)

        # Part A
        if r[1] is not None and r[0] != 200:
            A = False

        # Part B
        try:
            if assert_valid_schema(r[1], 'json_format/landingPage.json'):
                B = False
        except Exception as e:
            B = False
            messages.append(e)

        if A and B:
            result = True
            return result, messages
        else:
            result = False
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")

        return result, messages

    @staticmethod
    def req_03_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)
        contents = r[1]
        links = contents.get("links")
        for link in links:
            if not is_url_ok(link["href"], MediaType.JSON):
                result = False
                messages.append("Link {} did not return a valid response to a GET request".format(link["href"]))

        return result, messages

    @staticmethod
    def req_04_test(api_base_url: str):
        result = True
        messages = []
        # get the service-desc URL
        # get the service-doc URL
        r = get_url_content(api_base_url, MediaType.JSON)

        for link in r[1]["links"]:
            if link["rel"] == "service-desc":
                service_desc_uri = link["href"]
                service_desc_type = [x for x in MediaType if link["type"] == x.value][0]
            elif link["rel"] == "service-doc":
                service_doc_uri = link["href"]
                service_doc_type = [x for x in MediaType if link["type"] == x.value][0]

        # call each
        if not is_url_ok(service_desc_uri, service_desc_type):
            result = False
            messages.append("service-desc link did not return a value")
        else:
            r2 = get_url_content(service_desc_uri, service_desc_type)
            if not r2[2]["Content-Type"].startswith(str(service_desc_type)):
                if not r2[2]["Content-Type"].startswith("application/json"):
                    result = False
                    messages.append("service-desc link did not return the correct Content-Type")

        if not is_url_ok(service_doc_uri, service_doc_type):
            result = False
            messages.append("service-doc link did not return a value")
        else:
            if not r2[2]["Content-Type"].startswith(str(service_doc_type)):
                if not r2[2]["Content-Type"].startswith("application/json"):
                    result = False
                    messages.append("service-doc link did not return the correct Content-Type")

        return result, messages

    @staticmethod
    def req_05_test(api_base_url: str):
        messages = []
        result = True

        if not is_url_ok(api_base_url + "/conformance"):
            messages.append(
                "API Conformance URI, {}/conformance, does not respond to a GET request".format(api_base_url))
            result = False
        return result, messages

    @staticmethod
    def req_06_test(api_base_url: str):
        A = True
        B = True
        messages = []

        r = get_url_content(api_base_url + "/conformance", MediaType.JSON)  # could also have been MediaType.JSON
        if r[1] is not None and r[0] != 200:
            result = False
            A = False
            messages.append(
                "Content was returned for the Conformance endpoint, {}, but the response code was incorrect. "
                "It was {}, should have been 200".format(api_base_url + "/conformance", r[0]))

        # Part B
        try:
            if assert_valid_schema(r[1], 'json_format/confClasses.json'):
                B = False
        except Exception as e:
            B = False
            messages.append(e)

        if A and B:
            result = True
            return result, messages
        else:
            result = False
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_07_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)  # could also have been MediaType.JSON
        if r[1] is not None and r[0] != 200:
            result = False
            messages.append("Content was returned for the endpoint, {}, but the response code was incorrect. "
                            "It was {}, should have been 200".format(api_base_url + "/conformance", r[0]))

        return result, messages

    @staticmethod
    def req_08_test(api_base_url: str):
        messages = []
        result = True

        r = get_url_content(api_base_url + "?_broken=param")
        if r[0] != 400:
            messages.append("API landing page URI, {}, does not respond to a bad parameter with an HTTP 400 status code"
                            .format(api_base_url))
            result = False

        r = get_url_content(api_base_url + "/collections?_broken=param")
        if r[0] != 400:
            messages.append("API Collections URI, {}, does not respond to a bad parameter with an HTTP 400 status code"
                            .format(api_base_url + "/collections"))
            result = False

        return result, messages

    @staticmethod
    def req_09_test(api_base_url: str):
        messages = []
        result = True

        r = get_url_content(api_base_url + "&my_first_parameter=some%20value&my_other_parameter=42")
        if r[0] != 400:
            messages.append("API URI, {}, does not respond to a bad parameter with an HTTP 400 status code."
                            .format(api_base_url + "&my_first_parameter=some%20value&my_other_parameter=42"))
            result = False

        return result, messages

    @staticmethod
    def req_10_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_11_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Status code for {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages
        return result, messages

    @staticmethod
    def req_12_test(api_base_url: str):
        A = True
        B = True
        messages = []

        # get the GeoSPARQL RDF representation of a Feature, check for CRS
        # Part A
        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        # Part B
        try:
            if assert_valid_schema(r[1], 'json_format/collections.json'):
                B = False
        except Exception as e:
            B = False
            messages.append(e)

        if A and B:
            result = True
            return result, messages
        else:
            result = False
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_13_test(api_base_url: str):
        A = True
        B = True
        messages = []

        # get the GeoSPARQL RDF representation of a Feature, check for CRS
        # Part A
        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        for link in r[1]['links']:
            if 'self' not in link.values() or 'alternate' not in link.values():
                A = False
                messages.append('Link self or alternate do not found.')
        # Part B
        try:
            for link in r[1]['links']:
                if 'rel' not in link or 'type' not in link:
                    B = False
                    messages.append('Link {} does not include rel or type parameters.'.format(link))
        except Exception as e:
            B = False
            messages.append(e)

        if A and B:
            result = True
            return result, messages
        else:
            result = False
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_14_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if r[1].get("collections"):
            result = False
            messages.append("Items not found in collections.")
        return result, messages

    @staticmethod
    def req_15_test(api_base_url: str):
        A = True
        B = True
        messages = []

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        # Part B
        if not r[1]['collections']:
            A = False
            messages.append("Empty collections")

        for collection in r[1]['collections']:
            if 'links' not in collection:
                A = False
                messages.append("Collection {} does not include links property".format(collection))

            if 'rel' not in collection['links'] or 'type' not in collection['links']:
                B = False
                messages.append('Link {} does not include rel or type properties.'.format(collection['links']))

        if A and B:
            result = True
            return result, messages
        else:
            result = False
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_16_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if not r[1]['collections']:
            result = False
            messages.append("Empty collections")

        for collection in r[1]['collections']:
            if 'extent' not in collection:
                result = False
                messages.append("Collection {} does not include extent properties".format(collection))
                return result, messages
            if 'temporal' not in collection['extent'] or 'spatial' not in collection['extent']:
                result = False
                messages.append(
                    "Collection {} does not include temporal or spatial properties".format(collection['extent']))
                return result, messages
        return result, messages

    @staticmethod
    def req_17_test(api_base_url: str):
        # TODO: Finish collections id - PART B
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        api_base_url = "http://provinces.surroundaustralia.com/"

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if not r[1]['collections']:
            result = False
            messages.append("Empty collections")
            return result, messages

        for collection in r[1]['collections']:
            r = is_url_ok(
                api_base_url + "/collections/{}".format(collection['id']))  # could also have been MediaType.JSON
            if r[1] is not None and r[0] != 200:
                result = False
                messages.append(
                    "Content was returned for the Collections endpoint, {}, but the response code was incorrect. "
                    "It was {}, should have been 200".format(api_base_url + "/collections", r[0]))
                return result, messages

    @staticmethod
    def req_18_test(api_base_url: str):
        # TODO: Finish collections id - PART B
        A = True
        B = True
        result = True
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        api_base_url = "http://provinces.surroundaustralia.com/"

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if not r[1]['collections']:
            result = False
            messages.append("Empty collections")
            return result, messages

        return result, messages

    @staticmethod
    def req_19_test(api_base_url: str):
        # TODO: Finish collections id - PART B
        result = True
        A = True
        B = True
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        api_base_url = "http://provinces.surroundaustralia.com/"

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if not r[1]['collections']:
            result = False
            messages.append("Empty collections")
            return result, messages

        for collection in r[1]['collections']:
            r = get_url_content(api_base_url + "/collections/{}/items".format(collection['id']), MediaType.JSON)
            if r[0] != 200:
                messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                    api_base_url + "/collections"))
                result = False
                return result, messages

    @staticmethod
    def req_20_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_21_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_22_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_23_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_24_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_25_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_26_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_27_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_28_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_29_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_30_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_31_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_32_test(api_base_url: str):
        # TODO: Finish collections id - PART B
        result = False
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        api_base_url = "http://provinces.surroundaustralia.com/"

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                api_base_url + "/collections"))
            result = False
            return result, messages

        if not r[1]['collections']:
            result = False
            messages.append("Empty collections")
            return result, messages

        for collection in r[1]['collections']:
            r = get_url_content(api_base_url + "/collections/{}".format(collection['identifier']), MediaType.JSON)
            if r[0] != 200:
                messages.append("Error {}. It seems that it cannot list the items in /collections".format(
                    api_base_url + "/collections"))
                result = False
                return result, messages

        # TODO: It seems that I cannot obtain the items programatically from: http://provinces.surroundaustralia.com/collections/agp/items
        return result, messages

    @staticmethod
    def req_33_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_34_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_35_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url, MediaType.HTML)

        # Part A
        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.HTML. It seems that it cannot list the items in /collections".format(
                    api_base_url))
        return result, messages

    @staticmethod
    def req_36_test(api_base_url: str):
        result = True
        messages = []

        r = get_url_content(api_base_url, MediaType.HTML)

        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.HTML. It seems that it cannot list the items in /collections".format(
                    api_base_url))

        if not bool(BeautifulSoup(r[1], "html.parser").find()):
            result = False
            messages.append("It seems that {} has not html format.".format(api_base_url))
        return result, messages

    @staticmethod
    def req_37_test(api_base_url: str):
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)

        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.HTML. It seems that it cannot list the items in /collections".format(
                    api_base_url))
            return result, messages

        r = get_url_content(api_base_url + 'collections/agp/items/PR20119', MediaType.GEOJSON)
        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.GEOJSON. It seems that it cannot list the items in /collections".format(
                    api_base_url))
            return result, messages

    @staticmethod
    def req_38_test(api_base_url: str):
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)

        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.HTML. It seems that it cannot list the items in /collections".format(
                    api_base_url))
            return result, messages

        r = get_url_content(api_base_url + 'collections/agp/items/PR20119', MediaType.GEOJSON)
        if r[1] is not None and r[0] != 200:
            result = False
            messages.append(
                "Status code for {} with MediaType.HTML. It seems that it cannot list the items in /collections".format(
                    api_base_url))
            return result, messages

    @staticmethod
    def req_39_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_40_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_41_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_42_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_43_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_44_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_45_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_46_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_47_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_48_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_49_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages

    @staticmethod
    def req_50_test(api_base_url: str):
        result = False
        messages = ["Not implemented"]
        return result, messages


def format_for_results(requirement_no, r):
    return requirement_no, "PASS" if r[0] else "FAIL", r[1] if r[1] is not None else ""


def main(api_base_url):
    method_no = 0
    tests_list = [method for method in dir(RequirementTests) if method.startswith('__') is False]
    pass_tests = 0
    for test in tests_list:
        method_no += 1
        r = getattr(RequirementTests, test)(api_base_url)
        # rs.append(format_for_results(method_no, r))
        if r[0]:
            pass_tests += 1
        print(format_for_results(method_no, r))
    print("\nTotal passed tests: {} - Total tests: {}".format(pass_tests, len(tests_list)))
    return


if __name__ == "__main__":
    # for res in main("http://provinces.surroundaustralia.com/"):  # sys.argv[1]
    main("http://asgs.surroundaustralia.com")
