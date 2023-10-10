#!/usr/bin/python3
from models.engine.file_storage import FileStorage
"""import filestorage to handle data"""

"""Create a unique FileStorage instance"""
storage = FileStorage()

""" Call the reload() method to load data from the JSON file """
storage.reload()
