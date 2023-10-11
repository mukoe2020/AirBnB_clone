#!/usr/bin/python3
import json


class FileStorage:
    """ Private class attributes """
    __file_path = "file.json"
    __objects = {}  

    """ Public instance methods """
    @classmethod
    def all(cls):
        return cls.__objects

    @classmethod
    def new(cls, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        cls.__objects[key] = obj

    @classmethod
    def save(cls):
        serialized_objects = {}
        for key, value in cls.__objects.items():
            serialized_objects[key] = value.to_dict()

        with open(cls.__file_path, mode="w", encoding="utf-8") as file:
            json.dump(serialized_objects, file)

    @classmethod
    def reload(cls):
        try:
            with open(cls.__file_path, mode="r", encoding="utf-8") as file:
                deserialized_objects = json.load(file)

            for key, value in deserialized_objects.items():
                class_name, obj_id = key.split(".")

        except FileNotFoundError:
            pass
