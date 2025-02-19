import requests
import logging
import sys


def main():
    logger = logging.getLogger(__name__)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_formatter = logging.Formatter("[%(levelname)s] %(funcName)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    stdout_handler.setFormatter(stdout_formatter)

    # добавление обработчика к логгеру
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)

    request_data = 'test text'

    response = requests.get("http://127.0.0.1:5001/guess?text=", request_data).text
    logger.debug(input)
    logger.info('Flask response: ' + response)

    response2 = requests.get("http://127.0.0.1:5002/predict?text=" + request_data).text
    logger.info('FastAPI response: ' + response2)


if __name__ == '__main__':
    main()