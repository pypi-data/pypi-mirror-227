from datetime import datetime, timezone
import json
from typing import Dict, Any

class JSONStructureLogMessage:
    def __init__(self, message: str, level: str = "NOTSET!!", **kwargs):
        self.data = {}
        self.message = message
        self.level = level
        self.datetime = datetime.now(tz=timezone.utc)
        self.timestamp = self.datetime.timestamp()
        self.utcString = self.datetime.isoformat()
        self.data["level"] = level
        self.data["timestamp"] = self.timestamp
        self.data["message"] = self.message
        self.data["utcString"] = self.datetime.isoformat()
        # python 9 added the ability to do this: self.data = self.data | kwargs
        # TODO: feel like there is probably a faster way to combine these dict, or to handle this issue generally
        if kwargs is not None:
            self.context = kwargs
            return

        self.context = {}

    def add_property(self, name: str, value: Any):
        '''
        Used to add properties to a log message
        
        @property name => The name of the property.
        @property  value => The value of the property.
        '''
        self.context[name] = value

    def add_dict(self, data: Dict[str, Any]):
        '''
        Used to add an entire dictionary to the existing log message context.

        @property data => A dictionary to add the the log messages existing context
        '''
        self.context = {**self.context, **data}
        
    def __str__(self) -> str:
        '''
        Renders log message as a JSON string.
        '''
        log_data = self.data
        log_data["context"] = self.context
        return json.dumps(log_data)