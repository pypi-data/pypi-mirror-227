from structured_logging import StructuredLogger
import logging

def raise_err():
    raise Exception("BOOM")

if __name__ == "__main__":
    logger = StructuredLogger.get_default_logger("calvin", logging.DEBUG, {"parent-context": "This is cool!"})
    logger.debug("debug test")
    child_logger = logger.make_child_context_logger("calvin-child", {"child-context": "woo hoo!"})
    err = KeyError("uh oh")
    child_logger.info("an error", exc_info=err, stack_info=True, extra={"value1": 123, "value2": {"value3" :"456"}})
    try:
        raise_err()
    except Exception as e:
        logger.exception("testing exception logging")
        logger.warn("test with warning", exc_info=e)
        logger.warn("test with warning", is_exception_call=True)
