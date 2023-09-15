import pathlib

LOG_FORMAT = "%(levelname)s [%(module)s.%(funcName)s]: %(message)s"
BASE_PATH = str(pathlib.Path(__file__).parent.resolve())
