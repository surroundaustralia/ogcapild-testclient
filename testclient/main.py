import logging
from config import start_logger
import argparse
from specification import REQUIREMENTS


def main(args=None):
    # START setup
    start_logger()

    logging.info("OGC API LD Test Client started")

    parser = argparse.ArgumentParser()
    parser.add_argument("api_home", help="The web address (URL) stating point (home) of the API")
    args = parser.parse_args()
    logging.info(f"API Home is {args.api_home}")
    # END setup

    # START core tests
    results = []
    print("Testing core Requirements")
    for i, test in enumerate(REQUIREMENTS["core"]):
        # parts = []
        # for k, v in test["parts"].items():
        #     parts.append("{}: {}".format(k, v))
        #
        # logging.info("Testing {} {}".format(test["name"], test["id"]))
        # for part in parts:
        #     logging.info("\t\t" + part)

        print("Requirement {}".format(i))

        test_function = "req_{}_test".format(str(i+1).zfill(2))

        o = globals()[test_function](args.api_home)
        results.append({
            "id": test["id"],
            "outcome": o
        })
        logging.info("\t\t{}".format("PASS" if o[0] else "FAIL"))

        if not o[0]:
            logging.info("Ending due to test failure")
            break
    # END core tests

    logging.info("Aggregated results")
    for res in results:
        logging.info("{}: {}".format(res["id"], res["outcome"]))


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
