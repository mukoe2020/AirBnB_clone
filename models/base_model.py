#!/usr/bin/python3

"""Contains the class BaseModel that defines all common attributes/methods
 for other classes:
"""
import models
from datetime import datetime
import uuid


class BaseModel():
    """
    Defining parent class for future inheritance
    """

    def __init__(self, *args, **kwargs):
        """Initializing attributes of the instances of the class"""

        """generating random uuid and converting to a string format"""
        self.id = str(uuid.uuid4())

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)

                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.fromisoformat(value))

        else:
            models.storage.new(self)

    def __str__(self):
        """returns informal representation of an instance
        in the format [<class name>] (<self.id>) <self.__dict__>"""

        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__
        of the instance
        """

        resulting_dict = self.__dict__.copy()
        """
        created_at and updated_at converted to string object in ISO format
        """
        resulting_dict["created_at"] = self.created_at.isoformat()
        resulting_dict["updated_at"] = self.updated_at.isoformat()

        """
        a key __class__ must be added to this dictionary
        with the class name of the object
        """
        resulting_dict["__class__"] = self.__class__.__name__

        return resulting_dict