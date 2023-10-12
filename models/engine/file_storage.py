#!/usr/bin/python3

import json
import models
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """ this a file that serialize and deserialize object to json file  
    and from a json file  """
    file_path = "file.json"
    __objects = {}
    
    def all(self):
        """ Returns the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj


     def classes(self):
        """A list of valid classes"""
        from models.base_model import BaseModel
        from models.user import User
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.state import State
        from models.review import Review

        class_names {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def save(self):
        """ Serializes __objects to the JSON file (path: __file_path) """
        with open(FileStorage.file_path, "w") as file:
            objects_dict = {}
            for key, value in FileStorage.__objects.items():
                objects_dict[key] = value.to_dict()
            json.dump(objects_dict, file)


    def class_attributes(self):
        """Returns the valid attributes and their types for classname"""
        class_attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return class_attributes

    def reload(self):
        try:
            with open(FileStorage.file_path, 'r') as file:
                content = file.read()
                if content is None:
                    return
                objects_dict = json.loads(content)
                for key, value in objects_dict.items():
                    class_name, obj_id = key.split(".")
                    # Check if the object is already in __objects
                    obj_key = f"{class_name}.{obj_id}"
                    if obj_key not in FileStorage.__objects:
                        # If it's not in __objects, create and add the object
                        if class_name in FileStorage.class_names:
                            class_definition = FileStorage.class_names[class_name]
                            obj = class_definition(**value)
                            FileStorage.__objects[obj_key] = obj
        except FileNotFoundError:
            pass
