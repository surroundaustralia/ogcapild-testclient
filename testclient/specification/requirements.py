REQUIREMENTS = {
    "core": [
        {
            "name": "Requirement 1",
            "id": "/req/core/root-op",
            "parts": {
                "A": "The server SHALL support the HTTP GET operation at the path /."
            }
        },
        {
            "name": "Requirement 2",
            "id": "/req/core/root-success",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
                "B": """The content of that response SHALL be based upon the OpenAPI 3.0 schema landingPage.yaml and include at least links to the following resources:
    
    the API definition (relation type 'service-desc' or 'service-doc')
    
    /conformance (relation type 'conformance')
    
    /collections (relation type 'data')"""
            }
        },
        {
            "name": "Requirement 3",
            "id": "/req/core/api-definition-op",
            "parts": {
                "A": "The URIs of all API definitions referenced from the landing page SHALL support the HTTP GET method.",
            }
        },
        {
            "name": "Requirement 4",
            "id": "/req/core/api-definition-success",
            "parts": {
                "A": "A GET request to the URI of an API definition linked from the landing page (link relations service-desc or service-doc) with an Accept header with the value of the link property type SHALL return a document consistent with the requested media type.",
            }
        },
        {
            "name": "Requirement 5",
            "id": "/req/core/conformance-op",
            "parts": {
                "A": "The server SHALL support the HTTP GET operation at the path /conformance.",
            }
        },
        {
            "name": "Requirement 6",
            "id": "/req/core/conformance-success",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
                "B": "The content of that response SHALL be based upon the OpenAPI 3.0 schema confClasses.yaml and list all OGC API conformance classes that the server conforms to."
            }
        },
        {
            "name": "Requirement 7",
            "id": "/req/core/http",
            "parts": {
                "A": "The server SHALL conform to HTTP 1.1.",
                "B": "If the server supports HTTPS, the server SHALL also conform to HTTP over TLS."
            }
        },
        {
            "name": "Requirement 8",
            "id": "/req/core/query-param-unknown",
            "parts": {
                "A": "The server SHALL respond with a response with the status code 400, if the request URI includes a query parameter that is not specified in the API definition.",
            }
        },
        {
            "name": "Requirement 9",
            "id": "/req/core/query-param-invalid",
            "parts": {
                "A": "The server SHALL respond with a response with the status code 400, if the request URI includes a query parameter that has an invalid value.",
            }
        },
        {
            "name": "Requirement 10",
            "id": "/req/core/crs84",
            "parts": {
                "A": "Unless the client explicitly requests a different coordinate reference system, all spatial geometries SHALL be in the coordinate reference system http://www.opengis.net/def/crs/OGC/1.3/CRS84 (WGS 84 longitude/latitude) for geometries without height information and http://www.opengis.net/def/crs/OGC/0/CRS84h (WGS 84 longitude/latitude plus ellipsoidal height) for geometries with height information.",
            }
        },
        {
            "name": "Requirement 11",
            "id": "/req/core/fc-md-op",
            "parts": {
                "A": "The server SHALL support the HTTP GET operation at the path /collections.",
            }
        },
        {
            "name": "Requirement 12",
            "id": "/req/core/fc-md-success",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
                "B": "The content of that response SHALL be based upon the OpenAPI 3.0 schema collections.yaml."
            }
        },
        {
            "name": "Requirement 13",
            "id": "/req/core/fc-md-links",
            "parts": {
                "A": """A 200-response SHALL include the following links in the links property of the response:
    
    * a link to this response document (relation: self),
    
    * a link to the response document in every other media type supported by the server (relation: alternate).""",
                "B": "All links SHALL include the rel and type link parameters."
            }
        },
        {
            "name": "Requirement 14",
            "id": "/req/core/fc-md-items",
            "parts": {
                "A": "For each feature collection provided by the server, an item SHALL be provided in the property collections.",
            }
        },
        {
            "name": "Requirement 15",
            "id": "/req/core/fc-md-items-links",
            "parts": {
                "A": "For each feature collection included in the response, the links property of the collection SHALL include an item for each supported encoding with a link to the features resource (relation: items).",
                "B": "All links SHALL include the rel and type properties."
            }
        },
        {
            "name": "Requirement 16",
            "id": "/req/core/fc-md-extent",
            "parts": {
                "A": "For each feature collection, the extent property, if provided, SHALL provide bounding boxes that include all spatial geometries and time intervals that include all temporal geometries in this collection. The temporal extent may use null values to indicate an open time interval.",
                "B": "If a feature has multiple properties with spatial or temporal information, it is the decision of the server whether only a single spatial or temporal geometry property is used to determine the extent or all relevant geometries."
            }
        },
        {
            "name": "Requirement 17",
            "id": "/req/core/sfc-md-op",
            "parts": {
                "A": "The server SHALL support the HTTP GET operation at the path /collections/{collectionId}.",
                "B": "The parameter collectionId is each id property in the feature collections response (JSONPath: $.collections[*].id)."
            }
        },
        {
            "name": "Requirement 18",
            "id": "/req/core/sfc-md-success",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
                "B": "The content of that response SHALL be consistent with the content for this feature collection in the /collections response. That is, the values for id, title, description and extent SHALL be identical."
            }
        },
        {
            "name": "Requirement 19",
            "id": "/req/core/fc-op",
            "parts": {
                "A": "For every feature collection identified in the feature collections response (path /collections), the server SHALL support the HTTP GET operation at the path /collections/{collectionId}/items.",
                "B": "The parameter collectionId is each id property in the feature collections response (JSONPath: $.collections[*].id)."
            }
        },
        {
            "name": "Requirement 20",
            "id": "/req/core/fc-limit-definition",
            "parts": {
                "A": """The operation SHALL support a parameter limit with the following characteristics (using an OpenAPI Specification 3.0 fragment):
    
    name: limit
    in: query
    required: false
    schema:
      type: integer
      minimum: 1
      maximum: 10000
      default: 10
    style: form
    explode: false""",
            }
        },
        {
            "name": "Requirement 21",
            "id": "/req/core/fc-limit-response-1",
            "parts": {
                "A": "The response SHALL not contain more features than specified by the optional limit parameter. If the API definition specifies a maximum value for limit parameter, the response SHALL not contain more features than this maximum value.",
                "B": "Only items are counted that are on the first level of the collection. Any nested objects contained within the explicitly requested items SHALL not be counted."
            }
        },
        {
            "name": "Requirement 22",
            "id": "/req/core/fc-bbox-definition",
            "parts": {
                "A": """The operation SHALL support a parameter bbox with the following characteristics (using an OpenAPI Specification 3.0 fragment):
    
    name: bbox
    in: query
    required: false
    schema:
      type: array
      minItems: 4
      maxItems: 6
      items:
        type: number
    style: form
    explode: false""",
            }
        },
        {
            "name": "Requirement 23",
            "id": "/req/core/fc-bbox-response",
            "parts": {
                "A": "Only features that have a spatial geometry that intersects the bounding box SHALL be part of the result set, if the bbox parameter is provided.",
                "B": "If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries.",
                "C": "The bbox parameter SHALL match all features in the collection that are not associated with a spatial geometry, too.",
                "D": """The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (height or depth):
    
    * Lower left corner, coordinate axis 1
    * Lower left corner, coordinate axis 2
    * Minimum value, coordinate axis 3 (optional)
    * Upper right corner, coordinate axis 1
    * Upper right corner, coordinate axis 2
    * Maximum value, coordinate axis 3 (optional)
    """,
                "E": "The bounding box SHALL consist of four numbers and the coordinate reference system of the values SHALL be interpreted as WGS 84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in a parameter bbox-crs.",
                "F": "The coordinate values SHALL be within the extent specified for the coordinate reference system.",
            }
        },
        {
            "name": "Requirement 24",
            "id": "/req/core/fc-time-definition",
            "parts": {
                "A": """The operation SHALL support a parameter datetime with the following characteristics (using an OpenAPI Specification 3.0 fragment):
    
    name: datetime
    in: query
    required: false
    schema:
      type: string
    style: form
    explode: false
    """,
            }
        },
        {
            "name": "Requirement 25",
            "id": "/req/core/fc-time-response",
            "parts": {
                "A": "Only features that have a temporal geometry that intersects the temporal information in the datetime parameter SHALL be part of the result set, if the parameter is provided.",
                "B": "If a feature has multiple temporal properties, it is the decision of the server whether only a single temporal property is used to determine the extent or all relevant temporal properties.",
                "C": "The datetime parameter SHALL match all features in the collection that are not associated with a temporal geometry, too.",
                "D": """Temporal geometries are either a date-time value or a time interval. The parameter value SHALL conform to the following syntax (using ABNF):
    
    interval-closed     = date-time "/" date-time
    interval-open-start = [".."] "/" date-time
    interval-open-end   = date-time "/" [".."]
    interval            = interval-closed / interval-open-start / interval-open-end
    datetime            = date-time / interval
    """,
                "E": "The syntax of date-time is specified by RFC 3339, 5.6.",
                "F": "Open ranges in time intervals at the start or end are supported using a double-dot (..) or an empty string for the start/end.",
            }
        },
        {
            "name": "Requirement 26",
            "id": "/req/core/fc-response",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
                "B": "The response SHALL only include features selected by the request."
            }
        },
        {
            "name": "Requirement 27",
            "id": "/req/core/fc-links",
            "parts": {
                "A": """A 200-response SHALL include the following links:
                
    * a link to this response document (relation: self),
    * a link to the response document in every other media type supported by the service (relation: alternate).
    """,
            }
        },
        {
            "name": "Requirement 28",
            "id": "/req/core/fc-rel-type",
            "parts": {
                "A": "All links SHALL include the rel and type link parameters.",
            }
        },
        {
            "name": "Requirement 29",
            "id": "/req/core/fc-timeStamp",
            "parts": {
                "A": "If a property timeStamp is included in the response, the value SHALL be set to the time stamp when the response was generated.",
            }
        },
        {
            "name": "Requirement 30",
            "id": "/req/core/fc-numberMatched",
            "parts": {
                "A": "If a property numberMatched is included in the response, the value SHALL be identical to the number of features in the feature collections that match the selection parameters like bbox, datetime or additional filter parameters.",
                "B": "A server MAY omit this information in a response, if the information about the number of matching features is not known or difficult to compute."
            }
        },
        {
            "name": "Requirement 31",
            "id": "/req/core/fc-numberReturned",
            "parts": {
                "A": "If a property numberReturned is included in the response, the value SHALL be identical to the number of features in the response.",
                "B": "A server MAY omit this information in a response, if the information about the number of features in the response is not known or difficult to compute."
            }
        },
        {
            "name": "Requirement 32",
            "id": "/req/core/f-op",
            "parts": {
                "A": "For every feature in a feature collection (path /collections/{collectionId}), the server SHALL support the HTTP GET operation at the path /collections/{collectionId}/items/{featureId}.",
                "B": "The parameter collectionId is each id property in the feature collections response (JSONPath: $.collections[*].id). featureId is a local identifier of the feature."
            }
        },
        {
            "name": "Requirement 33",
            "id": "/req/core/f-success",
            "parts": {
                "A": "A successful execution of the operation SHALL be reported as a response with a HTTP status code 200.",
            }
        },
        {
            "name": "Requirement 34",
            "id": "/req/core/f-links",
            "parts": {
                "A": """A 200-response SHALL include the following links in the response:
    
    * a link to the response document (relation: self),
    * a link to the response document in every other media type supported by the service (relation: alternate), and
    * a link to the feature collection that contains this feature (relation: collection).
    """,
                "B": "All links SHALL include the rel and type link parameters."
            }
        },
    ],
    "html": [
        {
            "name": "Requirement 35",
            "id": "/req/html/definition",
            "parts": {
                "A": "Every 200-response of an operation of the server SHALL support the media type text/html.",
            }
        },
        {
            "name": "Requirement 36",
            "id": "/req/html/content",
            "parts": {
                "A": """Every 200-response of the server with the media type text/html SHALL be a HTML 5 document that includes the following information in the HTML body:

* all information identified in the schemas of the Response Object in the HTML <body>, and
* all links in HTML <a> elements in the HTML <body>.
""",
            }
        },
    ],
    "geojson": [
        {
            "name": "Requirement 37",
            "id": "/req/geojson/definition",
            "parts": {
                "A": """200-responses of the server SHALL support the following media types:

* application/geo+json for resources that include feature content, and
* application/json for all other resources.
""",
            }
        },
        {
            "name": "Requirement 38",
            "id": "/req/geojson/content",
            "parts": {
                "A": """Every 200-response with the media type application/geo+json SHALL be

* a GeoJSON FeatureCollection Object for features, and
* a GeoJSON Feature Object for a single feature.
""",
                "B": "The links specified in the requirements /req/core/fc-links and /req/core/f-links SHALL be added in a extension property (foreign member) with the name links.",
                "C": "The schema of all responses with the media type application/json SHALL conform with the JSON Schema specified for the resource in the Core requirements class."
            }
        },
        ],
    "gmlsf0": [
        {
            "name": "Requirement 39",
            "id": "/req/gmlsf0/definition",
            "parts": {
                "A": """200-responses of the server SHALL support the following media types:

* application/gml+xml; version=3.2; profile=http://www.opengis.net/def/profile/ogc/2.0/gml-sf0 for resources that include feature content,
* application/xml for all other resources.
""",
            }
        },
        {
            "name": "Requirement 40",
            "id": "/req/gmlsf0/content",
            "parts": {
                "A": "Table 3 specifies the XML document root element that the server SHALL return in a 200-response for each resource.",
                "B": "Every representation of a feature SHALL conform to the GML Simple Features Profile, Level 0 and be substitutable for gml:AbstractFeature.",
                "C": "The schema of all responses with a root element in the core namespace SHALL validate against the OGC API Features Core XML Schema.",
            }
        },
        {
            "name": "Requirement 41",
            "id": "/req/gmlsf0/headers",
            "parts": {
                "A": "If a property timeStamp is included in the response, its value SHALL be reported using the HTTP header named Date (see RFC 2616, 4.5).",
                "B": "If a property numberMatched is included in the response, its value SHALL be reported using an HTTP header named OGC-NumberMatched.",
                "C": "If a property numberReturned is included in the response, its value SHALL be reported using an HTTP header named OGC-NumberReturned.",
                "D": "If links are included in the response, each link SHALL be reported using an HTTP header named Link (see RFC 8288, Clause 3).",
            }
        },
        ],
    "gmlsf2": [
        {
            "name": "Requirement 42",
            "id": "/req/gmlsf2/definition",
            "parts": {
                "A": """200-responses of the server SHALL support the following media types:

* application/gml+xml; version=3.2; profile=http://www.opengis.net/def/profile/ogc/2.0/gml-sf2 for resources that include feature content,
* application/xml for all other resources.
""",
            }
        },
        {
            "name": "Requirement 43",
            "id": "/req/gmlsf2/content",
            "parts": {
                "A": """The requirement /req/gmlsf0/content applies, too, with the following changes:

* All references to media type application/gml+xml; version=3.2; profile=http://www.opengis.net/def/profile/ogc/2.0/gml-sf0 are replaced by application/gml+xml; version=3.2; profile=http://www.opengis.net/def/profile/ogc/2.0/gml-sf2.
* All references to "GML Simple Features Profile, Level 0" are replaced by "GML Simple Features Profile, Level 2".
""",
            }
        },
        {
            "name": "Requirement 44",
            "id": "/req/gmlsf2/headers",
            "parts": {
                "A": "The requirement /req/gmlsf0/content applies.",
            }
        },
    ],
    "oas30": [
        {
            "name": "Requirement 45",
            "id": "/req/oas30/oas-definition-1",
            "parts": {
                "A": "An OpenAPI definition in JSON using the media type application/vnd.oai.openapi+json;version=3.0 and a HTML version of the API definition using the media type text/html SHALL be available.",
            }
        },
        {
            "name": "Requirement 46",
            "id": "/req/oas30/oas-definition-2",
            "parts": {
                "A": "The JSON representation SHALL conform to the OpenAPI Specification, version 3.0.",
            }
        },
        {
            "name": "Requirement 47",
            "id": "/req/oas30/oas-impl",
            "parts": {
                "A": "The server SHALL implement all capabilities specified in the OpenAPI definition.",
            }
        },
        {
            "name": "Requirement 48",
            "id": "/req/oas30/completeness",
            "parts": {
                "A": "The OpenAPI definition SHALL specify for each operation all HTTP Status Codes and Response Objects that the server uses in responses.",
                "B": "This includes the successful execution of an operation as well as all error situations that originate from the server."
            }
        },
        {
            "name": "Requirement 49",
            "id": "/req/oas30/exceptions-codes",
            "parts": {
                "A": "For error situations that originate from the server, the API definition SHALL cover all applicable HTTP Status Codes.",
            }
        },
        {
            "name": "Requirement 50",
            "id": "/req/oas30/security",
            "parts": {
                "A": "For cases, where the operations of the server are access-controlled, the security scheme(s) SHALL be documented in the OpenAPI definition.",
            }
        },
    ]
}
