import json_log_formatter
import logging
from django.utils.timezone import now


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(
        self, message: str, extra: dict, record: logging.LogRecord
    ):

        data = {
            "message": message,
            "timestamp": now(),
            "level": record.levelname,
            "context": extra["data"] if "data" in extra else extra,
            "name": record.name,
            "filename": extra["file_name"]
            if "file_name" in extra
            else record.filename,
            "func_name": extra["func_name"]
            if "func_name" in extra
            else record.funcName,
            "msecs": record.msecs,
        }

        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)

        return data
