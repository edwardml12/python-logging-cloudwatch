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

        # ---- Elastic APM correlation IDs ----
        # These attrs are added by the Elastic APM Python agent
        trace_id = getattr(record, "elasticapm_trace_id", None)
        transaction_id = getattr(record, "elasticapm_transaction_id", None)
        span_id = getattr(record, "elasticapm_span_id", None)

        # Use ECS-compatible field names so Elastic can auto-link logs <-> traces
        # (these become top-level fields when your JSON is ingested)
        if trace_id:
            log_obj["trace.id"] = trace_id
        if transaction_id:
            log_obj["transaction.id"] = transaction_id
        if span_id:
            log_obj["span.id"] = span_id

        # Optional: include APM labels if you want extra context
        elastic_labels = getattr(record, "elasticapm_labels", None)
        if elastic_labels:
            # merge or nest; here we nest under "labels"
            log_obj.setdefault("labels", {}).update(elastic_labels)

        # return json.dumps(log_obj, indent=2)  # PRETTIFY JSON
        return json.dumps(log_obj)

logger = logging.getLogger("my_app")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.setLevel(logging.WARNING)
logger.addHandler(handler)
