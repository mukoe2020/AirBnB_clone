#!/usr/bin/python3
"""This module contains the HBNBCommand which
implements the cmd.Cmd class
"""


import cmd
import models
from models.user import User
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review

""" Create a dictionary mapping class names to class objects """
class_names = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'Review': Review
}


def list_objects(argument):
    """Returns objects in the storage in a list format"""

    objects = models.storage.all()
    list_objects = []
    for key, value in objects.items():
        if argument[0] == "":
            list_objects.append(str(value))
            continue
        if argument[0] == key[:len(argument[0])]:
            list_objects.append(str(value))
    return list_objects


def handle_parenthesis(argument):
    """ handles parenthesis and extracts argument within parenthesis"""

    if argument.find("(") + 1 == argument.find(")"):
        return "{}".format(argument[:argument.find(".")])

    return "{} {}".format(
        argument[:argument.find(".")],
        argument[argument.find(
            "(") + 1:-1].replace('"', '').replace(",", "")
        )


def updating_instance(instance, attr, attr_value):
    """Updates or adds attributes of an instance"""

    """Get the current value of the attribute 'attr' in 'instance'"""
    value = getattr(instance, attr, None)
    """Check if the attribute 'attr' exists in 'instance'"""
    if value is None:
        """if it does not, set the attribute with its value"""
        setattr(
            instance,
            attr, attr_value.replace('"', "")
        )
        """If it exists, determine the data type and update the attribute"""
    else:
        value_type = type(getattr(instance, attr))
        setattr(instance, attr,
                value_type(attr_value.replace('"', "")))


def updating_instance_with_dict(argument):
    """
     update an instance based on his ID with a dictionary:
     <class name>.update(<id>, <dictionary representation>)
    """

    argument_list = argument[
        argument.index("{") + 1:argument.index("}")
    ].replace(":", "").split(" ")
    arguments = argument[
        :argument.index("{")
    ].replace('"', '').replace(", ", "").replace(".update(", " ").split(" ")
    if len(arguments) == 0 or arguments[0] == "":
        print("** class name missing **")
    elif arguments[0] not in class_names:
        print("** class doesn't exist **")
    elif len(arguments) < 2:
        print("** instance id missing **")
    else:
        objects = models.storage.all()
        key = ".".join(arguments)
        if key in objects.keys():
            if len(argument_list) == 0:
                print("** attribute name missing **")
            elif len(arguments) % 2 != 0:
                print("** value missing **")
            else:
                instance = objects[key]
                for i in range(0, len(argument_list), 2):
                    updating_instance(
                        instance,
                        argument_list[i].replace("'", "").replace('"', ""),
                        argument_list[i + 1]
                    )
                instance.save()
        else:
            print("** no instance found **")


"""****************CONSOLE OR INTERPRETER METHODS***********************"""


class HBNBCommand(cmd.Cmd):
    """Contains the entry point of the command interpreter."""

    prompt = "(hbnb) "

    def onecmd(self, argument):
        """Handles user input such as User.all(), User.show(), User.count()
        and co
        """
        c = argument.split(".")
        if len(c) > 1:
            within_p = argument[argument.index(".") + 1:argument.index("(")]
            if within_p == "all":
                return self.do_all(argument[:argument.index(".")])
            elif within_p == "show":
                return self.do_show(handle_parenthesis(argument))
            elif within_p == "destroy":
                return self.do_destroy(handle_parenthesis(argument))
            elif within_p == "count":
                print(len(list_objects(handle_parenthesis(argument))))
                return
            elif within_p == "update":
                if argument.find("{") >= 0:
                    updating_instance_with_dict(argument)
                    return
                else:
                    return self.do_update(handle_parenthesis(argument))
        return super(HBNBCommand, self).onecmd(argument)

    def do_create(self, argument):
        """
        Creates a new instance of a class, saves it to the JSON file,
        and prints the ID.
        If the class name is missing or doesn't exist, it prints a message.
        """
        if not argument:
            print("** class name missing **")
        if argument not in class_names:
            print("** class doesn't exist **")
        else:
            new_instance = class_names[argument]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, argument):
        """
        Prints the string representation of an instance
        based on the class name and ID.
        """
        if not argument:
            print("** class name missing **")
        else:
            args = argument.split(" ")
            if args[0] not in class_names:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                objs = models.storage.all()
                key = f"{args[0]}.{args[1]}"
                if key in objs.keys():
                    print(objs[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, argument):
        """ Deletes an instance based on the class name and id
        (save the change into the JSON file)
        """
        if not argument:
            print("** class name missing **")
        else:
            args = argument.split(" ")
            if args[0] not in class_names:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                objs = models.storage.all()
                key = args[0] + "." + args[1]
                if key in objs.keys():
                    del objs[key]
                    models.storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, argument):
        """ Prints all string representation of all instances based
        or not on the class name"""
        objs = models.storage.all()

        args = argument.split(" ")

        if args[0] != "" and args[0] not in class_names:
            print("** class doesn't exist **")
        else:
            print(list_objects(args))

    def do_update(self, argument):
        """ Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the
        JSON file)
        """
        args = argument.split(" ")

        if args[0] == "":
            print("** class name missing **")
        elif args[0] not in class_names:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = args[0] + "." + args[1]
            objs = models.storage.all()
            if obj_key in objs.keys():
                if len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    instance = objs[obj_key]
                    setattr(instance, args[2], args[3])
                    instance.save()
            else:
                print("** no instance found **")

    def do_quit(self, argument):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, argument):
        """Indicates and implements the end of file condition"""
        print()
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass


"""prevents execution when code is imported"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()
