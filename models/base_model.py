#!/usr/bin/python3
"""Type module of BaseModel"""

import models
from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel():
    """
    Defining parent class for future inheritance"""


    def __init__(self, *args, **kwargs):
        """Type method initialize"""
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(val, timeformat))
                elif key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime and saves the instance using storage
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of dict
        of the instance
        """
        resulting_dict = self.__dict__.copy()
        resulting_dict["created_at"] = self.created_at.isoformat()
        resulting_dict["updated_at"] = self.updated_at.isoformat()
        resulting_dict["class"] = self.__class__.__name__
        
        return resulting_dict

    def __str__(self):
        """returns informal representation of an instance
        in the format [<class name>] (<self.id>) <self.to_dict>"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.to_dict())

