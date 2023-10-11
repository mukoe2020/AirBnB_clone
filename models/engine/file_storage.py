#!/usr/bin/python3
import json
import models
from models.base_model import BaseModel


class FileStorage:
    """ Private class attributes """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""

        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""

        key = str(type(obj).__name__) + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""

        with open(FileStorage.__file_path, "w") as file:
            objects_dict = {}
            for key, value in FileStorage.__objects.items():
                objects_dict[key] = FileStorage.__objects[key].to_dict()
            json.dump(objects_dict, file)

    def reload(self):
        try:
            with open(FileStorage.__file_path, 'r') as file:
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
                    class_definition = globals().get(class_name)
                    if class_definition:
                        obj = class_definition(**value)
                        FileStorage.__objects[obj_key] = obj
        except FileNotFoundError:
            pass
