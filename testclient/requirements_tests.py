import requests


def valid_link_object(link: dict):
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

            
def req_01_test(api_base_url: str):
    messages = []
    r = requests.get(
        api_base_url
    )
    if not r.ok:
        messages.append("API base URI, {}, does not respond to a GET request".format(api_base_url))
    return r.ok, None


def req_02_test(api_base_url: str):
    A = True
    B = True
    messages = []

    r = requests.get(
        api_base_url,
        headers={"Accept": "application/json"}
    )
    try:
        c = r.json()
    except:
        c = None

    if c is not None and r.status_code != 200:
        A = False

    try:
        title = c.get("title")
        if title is not None:
            if type(title) != str:
                B = False
                messages.append("The title property, since present, is not of type string, as required by the landingPage.yaml schema")
        description = c.get("description")
        if description is not None:
            if type(description) != str:
                B = False
                messages.append("The description property, since present, is not of type string, as required by the landingPage.yaml schema")
        links = c.get("links")
        if links is None:
            B = False
            messages.append("The links property must be present, as required by the landingPage.yaml schema")
        else:
            if type(links) != list:
                B = False
                messages.append("The links property is not of type list (array), as required by the landingPage.yaml schema")

            for link in links:
                link_valid = valid_link_object(link)
                if not link_valid[0]:
                    B = False
                    messages.append("A link on this page is not valid: {}".format("; ".join(link_valid[1])))

        # TODO: the API definition (relation type 'service-desc' or 'service-doc')
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


def req_03_test(api_base_url: str):
    result = True
    messages = []
    r = requests.get(
        api_base_url,
        headers={"Accept": "application/json"}
    )
    contents = r.json()
    links = contents.get("links")
    for link in links:
        r = requests.get(
            link["href"],
            headers={"Accept": "application/json"}
        )
        if not r.ok:
            result = False
            messages.append("Link {} did not return a valid response to a GET request".format(link["href"]))

    return result, messages


def req_04_test(api_base_url):
    result = True
    messages = []
    # get the service-desc URL
    # get the service-doc URL
    r = requests.get(
        api_base_url,
        headers={"Accept": "application/json"}
    )
    c = r.json()

    for link in c["links"]:
        if link["rel"] == "service-desc":
            service_desc_uri = link["href"]
            service_desc_type = link["type"]
        elif link["rel"] == "service-doc":
            service_doc_uri = link["href"]
            service_doc_type = link["type"]

    # call each
    r = requests.get(
        service_desc_uri,
        headers={"Accept": service_desc_type}
    )
    if not r.ok:
        result = False
        messages.append("service-desc link did not return a value")
    else:
        if not r.headers["Content-Type"].startswith(service_desc_type):
            result = False
            messages.append("service-desc link did not return the correct Content-Type")

    r = requests.get(
        service_doc_uri,
        headers={"Accept": service_doc_type}
    )
    if not r.ok:
        result = False
        messages.append("service-doc link did not return a value")
    else:
        if not r.headers["Content-Type"].startswith(service_doc_type):
            result = False
            messages.append("service-doc link did not return the correct Content-Type")

    return result, messages

"""
def req_05_test():
    pass


def req_06_test():
    pass


def req_07_test():
    pass


def req_08_test():
    pass


def req_09_test():
    pass


def req_10_test():
    pass


def req_11_test():
    pass


def req_12_test():
    pass


def req_13_test():
    pass


def req_14_test():
    pass


def req_15_test():
    pass


def req_16_test():
    pass


def req_17_test():
    pass


def req_18_test():
    pass


def req_19_test():
    pass


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


def format_for_results(requirement_no, result):
    return requirement_no, "PASS" if result[0] else "FAIL", "\n".join(result[1]) if result[1] is not None else ""


def main(api_base_url):
    results = []

    r01 = req_01_test(api_base_url)
    results.append(format_for_results(1, r01))
    if r01[0]:
        r02 = req_02_test(api_base_url)
        results.append(format_for_results(2, r02))
        if r02[0]:
            r03 = req_03_test(api_base_url)
            results.append(format_for_results(3, r03))
            if r03[0]:
                r04 = req_04_test(api_base_url)
                results.append(format_for_results(4, r04))

    for result in results:
        print(result)

    """
    req_02_test()
    req_03_test()
    req_04_test()
    req_05_test()
    req_06_test()
    req_07_test()
    req_08_test()
    req_09_test()
    req_10_test()
    req_11_test()
    req_12_test()
    req_13_test()
    req_14_test()
    req_15_test()
    req_16_test()
    req_17_test()
    req_18_test()
    req_19_test()
    req_20_test()
    req_21_test()
    req_22_test()
    req_23_test()
    req_24_test()
    req_25_test()
    req_26_test()
    req_27_test()
    req_28_test()
    req_29_test()   
    req_30_test()
    req_31_test()
    req_32_test()
    req_33_test()
    req_34_test()
    req_35_test()
    req_36_test()
    req_37_test()
    req_38_test()
    req_39_test()
    req_40_test()
    req_41_test()
    req_42_test()
    req_43_test()
    req_44_test()
    req_45_test()
    req_46_test()
    req_47_test()
    req_48_test()
    req_48_test()
    req_50_test()
    """
    
    
if __name__ == "__main__":
    main("http://localhost:5000")
