import logging
import sys
from typing import Dict, Any
import traceback

from .json_log_message import JSONStructureLogMessage

_default_stack_level_offset = -1



class StructuredLogger:
    def __init__(self, name: str, level: int = logging.WARN, context: Dict[str, Any] = {}, log_record_factory = JSONStructureLogMessage, is_child: bool = False):
        '''
        Constructor

        @property name => the name of the logger
        @property level => the logging level. is a 1 to 1 match to the logging levels in the logging package i.e. logging.INFO
        @property context => context at the logger level that will be added to all log messages written by this logger
        @property log_record_factory => A factory function that produces a structured log record to be serialized for logging. See JSONStructureLogMessage if you would like to have a structured log format other than JSON.
        '''
        self._log_record_factory = log_record_factory
        self.name = name
        self._level = level
        self._logger: logging.Logger = None
        self._context = context
        if not is_child:
            self._logger = logging.getLogger(name=name)
            self._logger.setLevel(level)

    def make_child_context_logger(self, name: str, context: Dict[str, Any] = {}):
        '''
        Used to make a child logger. Useful for having parent context included in child loggers. 
        One example where this is useful is for adding things like trace ids.

        @property name => The name of the child logger
        @property context => Context to add to the new logger. This context will be combined with the parent loggers context.
        '''
        combinedContext = {**self._context, **context}
        childLogger = StructuredLogger(name, self._level, combinedContext, self._log_record_factory)
        childLogger._logger = self._logger
        return childLogger

    def add_handler(self, handler: logging.Handler, set_default_formatter:bool = True):
        '''
        Used to add your own handlers. Want to log to a file or have different log handlers for different log levels?
        Just add them ;-)

        Leaving set_default_formatter to its default value of True is recommended to have the structure logging work properly
        '''
        if set_default_formatter:
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
        self._logger.addHandler(handler)
    
    def _log(
        self, 
        level: int,
        msg: object, 
        *args: object, 
        exc_info: Exception = None, 
        stack_info: bool = False, 
        stacklevel: int = 0, 
        extra: dict = {},
        is_exception_call: bool = False
        ):
        '''
        This is the wrapper method that calls the standard Logger from the logging package.
        The goal is for it to be backwards compatible with the standard logger logging methods.
        
        @property level => *See logging.Logger_log method?
        @property msg => *See logging.Logger_log method?
        @property *args => *See logging.Logger_log method?
        @property exc_info => *See logging.Logger_log method?
        @property stack_info => *See logging.Logger_log method?
        @property stacklevel => *See logging.Logger_log method?
        @property extra => *See logging.Logger_log method?
        @property is_exception_call => This is set to True for exception logs. It will automatically get exception info from traceback if exc_info is not provided.
        '''
        logMethod = None
        levelStr = ""
        if level == logging.CRITICAL:
            levelStr = "CRITICAL"
            logMethod = self._logger.critical
        elif level == logging.ERROR:
            levelStr = "ERROR"
            logMethod = self._logger.error
        elif level == logging.WARN:
            levelStr = "WARN"
            logMethod = self._logger.warn
        elif level == logging.WARNING:
            levelStr = "WARNING"
            logMethod = self._logger.warning
        elif level == logging.INFO:
            levelStr = "INFO"
            logMethod = self._logger.info
        else:
            levelStr = "DEBUG"
            logMethod = self._logger.debug
        
        context = {**self._context, **extra}
        self._set_exception_and_stack_info(context, exc_info=exc_info, include_stack=stack_info, limit=stacklevel, is_exception_call=is_exception_call)
        record = self._log_record_factory(msg, levelStr, **context)
        logMethod(record)


    def debug(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        # self._set_exception_and_stack_info(extra, exc_info=exc_info, include_stack=stack_info, limit=stacklevel, isExceptionCall=is_exception_call)
        self._log(logging.DEBUG, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def info(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        # self._set_exception_and_stack_info(extra, exc_info=exc_info, include_stack=stack_info, limit=stacklevel, isExceptionCall=is_exception_call)
        self._log(logging.INFO, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def warn(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        self._log(logging.WARN, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def warning(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        self._log(logging.WARNING, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def error(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        self._log(logging.ERROR, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def exception(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {}
            ):
        self._log(logging.ERROR, msg, *args, extra=extra, exc_info=exc_info, stack_info=False, stacklevel=None, is_exception_call=True)

    def critical(
            self, 
            msg: object, 
            *args: object, 
            exc_info: Exception = None, 
            stack_info: bool = False, 
            stacklevel: int = 0, 
            extra: dict = {},
            is_exception_call: bool = False
            ):
        self._log(logging.CRITICAL, msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, is_exception_call=is_exception_call)

    def _set_exception_and_stack_info(self, context: Dict[str, Any], exc_info = None, include_stack = False, limit = 0, is_exception_call = False):
        '''
        Sets exception info for a log message.

        @property context => The context object for the log message.
        @property exc_info => Exception from the log method being called.
        @property include_stack => If True stack info will be added to the context.
        @property limit => The Stack offset added to _default_stack_level_offset.
        @property is_exception_call => If True and exc_info is None traceback is used to get info on the last exception thrown.
        '''
        if exc_info is None:
            if is_exception_call:
                # set from traceback...
                context["exception"] = traceback.format_exc()
                include_stack = False
        elif isinstance(exc_info, BaseException):
            # handle exception parsing
            context["exception"] = traceback.format_exception(type(exc_info), exc_info, None)
            # TODO: find a way to get stack trace from exception
            # include_stack = False
        else:
            # Just write the string method output?
            context["exception"] = str(exc_info)

        if include_stack:
            context["stacktrace"] = traceback.format_stack(limit=_default_stack_level_offset+limit)

    @staticmethod
    def get_default_logger(name: str, log_level:int = logging.WARN, context: Dict[str, Any] = {}, use_stderr: bool = False):
        '''
        Helper function used to get a default console logger that writes to stdout (or stderr if use_stderr is set to True).

        @property name => The name of the logger.
        @property log_level => The log level for the logger.
        @property context => The context to attach to every log message this logger writes.
        @property use_stderr => If true logs will be written to stderr and not stdout.
        '''
        logger = StructuredLogger(name, log_level, context=context, log_record_factory=JSONStructureLogMessage)
        handler = logging.StreamHandler(sys.stdout if not use_stderr else sys.stderr)
        handler.setLevel(logging.NOTSET)
        logger.add_handler(handler, True)
        return logger
