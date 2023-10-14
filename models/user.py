#!/usr/bin/python3
""" the clas user module"""
from models.base_model import BaseModel


class User(BaseModel):
    """ User class definition """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
