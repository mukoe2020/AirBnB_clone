#!/usr/bin/python3

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


def handle_parenthesis(command):
    """ handles parenthesis and extracts command within parenthesis"""

    if command.find("(") + 1 == command.find(")"):
        return "{}".format(command[:command.find(".")])

    return "{} {}".format(
        command[:command.find(".")],
        command[command.find(
            "(") + 1:-1].replace('"', '').replace(",", "")
        )


class HBNBCommand(cmd.Cmd):
    """Contains the entry point of the command interpreter."""

    prompt = "(hbnb) "

    def onecmd(self, command):
        """Handles user input such as User.all(), User.show(), User.count()
        and co
        """
        c = command.split(".")
        if len(c) > 1:
            within_p = command[command.index(".") + 1:command.index("(")]
            if within_p == "all":
                return self.do_all(command[:command.index(".")])
            elif within_p == "show":
                return self.do_show(handle_parenthesis(command))
            elif within_p == "destroy":
                return self.do_destroy(handle_parenthesis(command))
            elif within_p == "count":
                print(len(list_objects(handle_parenthesis(command))))
                return
            elif within_p == "update":
                return self.do_update(handle_parenthesis(command))
        return super(HBNBCommand, self).onecmd(command)

    def do_quit(self, argument):
        """Quits the command interpreter"""
        return True

    def help_quit(self):
        """Help message for the quit command"""
        print("Quit command to exit the program\n")

    def do_EOF(self, argument):
        """Indicates and implements the end of file condition"""
        print()
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass

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
            print("** class name missing**")
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

        if not argument:
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


"""prevents execution when code is imported"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()
