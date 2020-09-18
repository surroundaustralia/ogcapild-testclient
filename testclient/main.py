from config import *
import argparse


def main(args=None):
    start_logger()

    logging.info("OGC API LD Test Client started")

    parser = argparse.ArgumentParser()
    parser.add_argument("api_home", help="The web address (URL) stating point (home) of the API")
    args = parser.parse_args()
    logging.info(f"API Home is {args.api_home}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
