import logging
from os.path import join, dirname, abspath


def start_logger(filename=None):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
        filename=filename if filename is not None else join(abspath(dirname(__file__)), "testclient.log"),
        filemode="w"
    )

    # set screen logging for levels > INFO
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logging.getLogger().addHandler(console)
