import logging


class FirstInfoMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.basicConfig(level=logging.INFO, filename="logging_file.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

        # logging.info(f"Domaine name {request.environ['DOMAIN']}")
        # logging.info(f"Body {request.body}")
        # logging.info(f"Headers {request.headers}")
        # logging.info(f"Query_params {request.GET}")
        # logging.info(f"Method {request.method}")

        request_log = {
            'type': 'request',
            'host': request.environ['DOMAIN'],
            'headers': request.headers,
            'body': request.body,
            'query_params': request.GET,
            'method': request.method,

        }

        logging.info(request_log)


        response = self.get_response(request)

        logging.info(f"status code response {response.status_code}")
        return response
