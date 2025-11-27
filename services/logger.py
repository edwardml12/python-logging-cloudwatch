import logging
import sys
import json
import traceback

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # If logger.error(..., exc_info=True) or logger.exception(...) was called
        if record.exc_info:
            # Split traceback into a list of lines (prettified)
            trace_list = traceback.format_exception(*record.exc_info)
            # Remove trailing newlines and strip
            log_obj["trace"] = [line.rstrip("\n") for line in trace_list]

        # return json.dumps(log_obj, indent=2)  # PRETTIFY JSON
        return json.dumps(log_obj)

logger = logging.getLogger("my_app")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.setLevel(logging.INFO)
logger.addHandler(handler)
