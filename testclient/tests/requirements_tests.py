import sys
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

        if r[1] is not None and r[0] != 200:
            A = False

        try:
            title = r[1].get("title")
            if title is not None:
                if type(title) != str:
                    B = False
                    messages.append("The title property, since present, is not of type string, as required by the "
                                    "landingPage.yaml schema")
            description = r[1].get("description")
            if description is not None:
                if type(description) != str:
                    B = False
                    messages.append("The description property, since present, is not of type string, as required by "
                                    "the landingPage.yaml schema")
            links = r[1].get("links")
            if links is None:
                B = False
                messages.append("The links property must be present, as required by the landingPage.yaml schema")
            else:
                if type(links) != list:
                    B = False
                    messages.append("The links property is not of type list (array), as required by the "
                                    "landingPage.yaml schema")

                for link in links:
                    link_valid = valid_link_object(link)
                    if not link_valid[0]:
                        B = False
                        messages.append("A link on this page is not valid: {}".format("; ".join(link_valid[1])))

            conformance = False
            collections = False
            for link in links:
                if link.get("rel") == "conformance":
                    if link.get("href").endswith("/conformance"):
                        conformance = True

                if link.get("rel") == "data":
                    if link.get("href").endswith("/collections"):
                        collections = True
            if not conformance:
                B = False
                messages.append("A link on this page of type 'conformance' to /conformance is not given")
            if not collections:
                B = False
                messages.append("A link on this page of type 'data' to /collections is not given")
        except Exception as e:
            B = False
            messages.append("An error occurred in parsing the content of the page according to the "
                            "landingPage.yaml schema: {}".format(e))

        # final result
        if A and B:
            result = True
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
            messages.append("API Conformance URI, {}/conformance, does not respond to a GET request".format(api_base_url))
            result = False
        return result, messages

    @staticmethod
    def req_06_test(api_base_url: str):
        result = True
        A = True
        B = True
        messages = []

        r = get_url_content(api_base_url + "/conformance", MediaType.JSON)  # could also have been MediaType.JSON
        if r[1] is not None and r[0] != 200:
            result = False
            A = False
            messages.append("Content was returned for the Conformance endpoint, {}, but the response code was incorrect. "
                            "It was {}, should have been 200".format(api_base_url + "/conformance", r[0]))

        conforms_to = r[1].get("conformsTo")
        if conforms_to is None:
            result = False
            B = False
            messages.append("The conformsTo property is not present")
        elif type(conforms_to) != list:
            result = False
            B = False
            messages.append("The conformsTo property is present but is not of type list (Array) "
                            "but instead of type {}".format(type(conforms_to)))

        if not A:
            messages.insert(0, "Part A failed")
        if not B:
            messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_07_test(api_base_url: str):
        # If we get to this test, the server will have already successfully responded to multiple GET & HEAD requests
        result = True
        messages = []
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

        # "A": "The server SHALL respond with a response with the status code 400, if the request URI includes a
        # query parameter that has an invalid value.",

        return result, messages

    @staticmethod
    # TODO: Fix problem with collections which cannot access any item in the response. No response
    def req_10_test(api_base_url: str):
        result = False
        messages = []
        # get the GeoSPARQL RDF representation of a Feature, check for CRS
        r = get_url_content(api_base_url + "/collections", MediaType.JSON)
        if r[0] != 200:
            messages.append("Status code for {}. It seems that it cannot list the items in /collections".format(api_base_url + "/collections"))
            result = False
            return result, messages

        first_col_id = r[1].get("collections")[0]["id"]
        r = get_url_content(api_base_url + "/collections/" + first_col_id + "/items")
        import pprint
        pprint.pprint(r[1])
        first_feature_id = r[1].get("collection")["features"][0]["id"]
        feature_url = api_base_url + "collections/" + first_col_id + "/items/" + first_feature_id
        param_string = "_profile=geosp"
        r = get_url_content(feature_url + "?" + param_string, MediaType.NT)
        for line in r[1].split(" ."):
            if "<https://linked.data.gov.au/def/geox#inCRS>" in line:
                result = True
        if not result:
            messages.append("")

        # r = get_turtle(feature_url + "?" + param_string)
        # print(r)
        return result, messages

    @staticmethod
    def req_11_test(api_base_url: str):
        messages = []

        r = get_url_content(api_base_url + "/collections")
        if r[0] != 200:
            messages.append("Response code was incorrect for {}. It was {}, should have been 200".format(api_base_url + "/collections", r[0]))
            result = False
            return result, messages
        result = True
        messages.append("")
        return result, messages

    @staticmethod
    def req_12_test(api_base_url: str):
        result = True
        A = True
        B = True
        messages = []

        r = get_url_content(api_base_url + "/collections", MediaType.JSON)  # could also have been MediaType.JSON
        if r[1] is not None and r[0] != 200:
            result = False
            A = False
            messages.append(
                "Content was returned for the Collections endpoint, {}, but the response code was incorrect. "
                "It was {}, should have been 200".format(api_base_url + "/collections", r[0]))

        # TODO: Compare yaml schema with result - PART B
        # conforms_to = r[1].get("conformsTo")
        # if conforms_to is None:
        #     result = False
        #     B = False
        #     messages.append("The conformsTo property is not present")
        # elif type(conforms_to) != list:
        #     result = False
        #     B = False
        #     messages.append("The conformsTo property is present but is not of type list (Array) "
        #                     "but instead of type {}".format(type(conforms_to)))

        if not A:
            messages.insert(0, "Part A failed")
        if not B:
            messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_13_test(api_base_url: str):
        messages = ["Not implemented - Fixed error with /collections endpoint"]
        result = False
        return result, messages

    @staticmethod
    def req_14_test(api_base_url: str):
        messages = ["Not implemented - Fixed error with /collections endpoint"]
        result = False
        return result, messages

    @staticmethod
    def req_15_test(api_base_url: str):
        messages = ["Not implemented - Fixed error with /collections endpoint"]
        result = False
        return result, messages

    @staticmethod
    def req_16_test(api_base_url: str):
        messages = ["Not implemented - Fixed error with /collections endpoint"]
        result = False
        return result, messages

    @staticmethod
    def req_17_test(api_base_url: str):
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        collectionId = ["agp"]

        for c in collectionId:
            A = True
            B = True
            result = True
            r = get_url_content(api_base_url + "/collections/{}".format(c), MediaType.JSON)  # could also have been MediaType.JSON
            if r[1] is not None and r[0] != 200:
                result = False
                A = False
                messages.append(
                    "Content was returned for the Collections endpoint, {}, but the response code was incorrect. "
                    "It was {}, should have been 200".format(api_base_url + "/collections", r[0]))

            if 'id' in r[1].get('collection'):
                if r[1].get('collection')['id'] == c:
                    result = True
                    B = True
                else:
                    result = False
                    B = False
                    messages.append("collection.id is not equal to collectionId {}".format(collectionId))
            else:
                result = False
                B = False
                messages.append("id property not found in .collections[*]")
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
            if not result:
                return result, messages

    @staticmethod
    def req_18_test(api_base_url: str):
        A = True
        B = True
        result = True
        messages = []

        r = get_url_content(api_base_url, MediaType.JSON)
        if r[1] is not None and r[0] != 200:
            result = False
            A = False
            messages.append(
                "Content was returned for the Collections endpoint, {}, but the response code was incorrect. "
                "It was {}, should have been 200".format(api_base_url + "/collections", r[0]))

        # TODO: Compare yaml schema with result - PART B
        B = False
        # conforms_to = r[1].get("conformsTo")
        # if conforms_to is None:
        #     result = False
        #     B = False
        #     messages.append("The conformsTo property is not present")
        # elif type(conforms_to) != list:
        #     result = False
        #     B = False
        #     messages.append("The conformsTo property is present but is not of type list (Array) "
        #                     "but instead of type {}".format(type(conforms_to)))
        if not A:
            messages.insert(0, "Part A failed")
        if not B:
            messages.insert(0, "Part B failed")
        return result, messages

    @staticmethod
    def req_19_test(api_base_url: str):
        result = True
        A = True
        B = True
        messages = []

        # TODO: When collections endpoint is properly working. Send get request to receive all collections id.
        collectionId = ["agp"]

        for c in collectionId:
            A = True
            B = True
            result = True
            r = get_url_content(api_base_url + "/collections/{}".format(c),
                                MediaType.JSON)  # could also have been MediaType.JSON
            if r[1] is not None and r[0] != 200:
                result = False
                A = False
                messages.append(
                    "Content was returned for the Collections endpoint, {}, but the response code was incorrect. "
                    "It was {}, should have been 200".format(api_base_url + "/collections", r[0]))

            if 'id' in r[1].get('collection'):
                if r[1].get('collection')['id'] == c:
                    result = True
                    B = True
                else:
                    result = False
                    B = False
                    messages.append("collection.id is not equal to collectionId {}".format(collectionId))
            else:
                result = False
                B = False
                messages.append("id property not found in .collections[*]")
            if not A:
                messages.insert(0, "Part A failed")
            if not B:
                messages.insert(0, "Part B failed")
            if not result:
                return result, messages


"""
def req_20_test():
    pass


def req_21_test():
    pass


def req_22_test():
    pass


def req_23_test():
    pass


def req_24_test():
    pass


def req_25_test():
    pass


def req_26_test():
    pass


def req_27_test():
    pass


def req_28_test():
    pass


def req_29_test():
    pass


def req_30_test():
    pass


def req_31_test():
    pass


def req_32_test():
    pass


def req_33_test():
    pass


def req_34_test():
    pass


def req_35_test():
    pass


def req_36_test():
    pass


def req_37_test():
    pass


def req_38_test():
    pass


def req_39_test():
    pass


def req_40_test():
    pass


def req_41_test():
    pass


def req_42_test():
    pass


def req_43_test():
    pass


def req_44_test():
    pass


def req_45_test():
    pass


def req_46_test():
    pass


def req_47_test():
    pass


def req_48_test():
    pass


def req_48_test():
    pass


def req_50_test():
    pass
"""


def format_for_results(requirement_no, r):
    return requirement_no, "PASS" if r[0] else "FAIL", r[1] if r[1] is not None else ""


def main(api_base_url):
    rs = []
    method_no = 0
    tests_list = [method for method in dir(RequirementTests) if method.startswith('__') is False]
    for test in tests_list:
        method_no += 1
        r = getattr(RequirementTests, test)(api_base_url)
        rs.append(format_for_results(method_no, r))
    return rs


if __name__ == "__main__":
    for res in main("http://provinces.surroundaustralia.com/"):  # sys.argv[1]
        print(res)
