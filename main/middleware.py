import logging
import sys
import json
import traceback

LOGGER = logging.getLogger("django")


class ExceptionLoggingMiddleware(object):
    """
    This middleware provides logging of exception in requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        Processes exceptions during handling of a http request.
        Logs them with *ERROR* level.
        """
        _, _, trace = sys.exc_info()
        extra = getattr(request, request.method, None)
        parsed_data = extra.__dict__ if extra is not None else {}

        tb_desc = traceback.extract_tb(trace)
        tb_file, tb_line_num, tb_function, tb_text = tb_desc[-1]

        LOGGER.error(
            """Processing exception %s at %s.
            %s""",
            exception,
            request.path,
            request.method,
            extra={
                "data": json.dumps(parsed_data),
                "file_name": tb_file,
                "func_name": tb_function,
            },
        )
        return None
