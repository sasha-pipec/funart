import logging
from datetime import datetime

# logger = logging.getLogger(__name__)
class FirstInfoMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response


    def __call__(self, request):

        logging.basicConfig(level=logging.INFO, filename="logging_file.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")
        # logger.info('START')

        logging.info(f"Domaine name {request.environ['DOMAIN']}")
        logging.info(f"Body {request.body}")
        logging.info(f"Headers {request.headers}")
        logging.info(f"Query_params {request.GET}")
        logging.info(f"Method {request.method}")

        response = self._get_response(request)

        logging.info(f"status code {response.status_code}")
        return response