#!/usr/bin/python3

""" Test module for base_model module """


from models.user import User
import unittest
from datetime import datetime
import io
import sys


class TestUser(unittest.TestCase):
    """ A TestCase class for the  User class """

    def test_initialization(self):
        """ test for initialization of the User class """

        model = User()
        self.assertIsInstance(model, User)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertIsInstance(model.email, str)
        self.assertIsInstance(model.password, str)
        self.assertIsInstance(model.first_name, str)
        self.assertIsInstance(model.last_name, str)
        self.assertEqual(model.email, "")
        self.assertEqual(model.password, "")
        self.assertEqual(model.first_name, "")
        self.assertEqual(model.last_name, "")

        model = User("name")
        self.assertIsInstance(model, User)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

        model.name = "John"
        model_dict = model.to_dict()
        model1 = User(**model_dict)
        self.assertIsInstance(model1, User)
        self.assertIsInstance(model1.id, str)
        self.assertIsInstance(model1.created_at, datetime)
        self.assertIsInstance(model1.updated_at, datetime)
        self.assertEqual(model.id, model1.id)
        self.assertEqual(model.name, model1.name)
        self.assertEqual(model.created_at, model1.created_at)
        self.assertEqual(model.updated_at, model1.updated_at)
        self.assertFalse(isinstance(getattr(model, "__class__", None), str))

        model1 = User(
            id=model_dict["id"], name="James",
            created_at=model_dict["created_at"])
        self.assertIsInstance(model1, User)
        self.assertIsInstance(model1.id, str)
        self.assertIsInstance(model1.created_at, datetime)
        self.assertTrue(
            isinstance(getattr(model1, "updated_at", None), datetime))
        self.assertEqual(model.id, model1.id)
        self.assertNotEqual(model.name, model1.name)
        self.assertEqual(model.created_at, model1.created_at)
        self.assertNotEqual(
            getattr(model1, "updated_at", None), model.updated_at)

        with self.assertRaises(ValueError) as ctx:
            model1 = User(
                id=model_dict["id"], name="James",
                created_at=model_dict["created_at"],
                updated_at="this is a bad date string")
        self.assertRegex(
            str(ctx.exception),
            "Invalid isoformat string: 'this is a bad date string'")

    def test_save_instance_method(self):
        """ test the save instance method of the User class """

        model = User()
        date1 = model.updated_at
        model.save()
        date2 = model.updated_at
        self.assertNotEqual(date1, date2)

    def test_to_dict_instance_method(self):
        """ test the to_dict instance method of the User Class """

        model = User()
        m_dict = model.to_dict()
        m_dict_keys = {"__class__", "id", "created_at", "updated_at"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["id"], str)
        self.assertIsInstance(m_dict["created_at"], str)
        self.assertIsInstance(m_dict["updated_at"], str)

        model = User()
        model.name = "John"
        model.age = 50
        m_dict = model.to_dict()
        m_dict_keys = {
            "__class__", "id", "created_at", "updated_at", "name", "age"}
        self.assertIsInstance(m_dict, dict)
        self.assertSetEqual(set(m_dict.keys()), m_dict_keys)
        self.assertIsInstance(m_dict["name"], str)
        self.assertIsInstance(m_dict["age"], int)

        with self.assertRaises(TypeError):
            m_dict = model.to_dict("argument")

    def test_str_representation(self):
        """ test the __str__ function of the User """

        model = User()
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        print(model)

        m_str = new_stdout.getvalue()
        self.assertIn("[User]", m_str)
        self.assertIn("'id': ", m_str)
        self.assertIn("'created_at': datetime.datetime", m_str)
        self.assertIn("'updated_at': datetime.datetime", m_str)
        self.assertEqual(
            f"[{model.__class__.__name__}] ({model.id}) {model.__dict__}\n",
            m_str)
        sys.stdout = sys.__stdout__
