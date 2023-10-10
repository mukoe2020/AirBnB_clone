#!/usr/bin/python3

import cmd
import models
from models.base_model import BaseModel

""" Create a dictionary mapping class names to class objects """
class_names = {
    'BaseModel': BaseModel
}


class HBNBCommand(cmd.Cmd):
    """
    contains the entry point of the command interpreter:
    """

    prompt = "(hbnb) "

    def do_quit(self, argument):
        """Quits the command intrepreter"""

        return True

    def help_quit(self):
        """help message for the quit command"""

        print("Quit command to exit the program\n")

    def do_EOF(self, argument):
        """Indicates and implements the end of file condition"""
        print()
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, argument):
        """Creates a new instance of BaseModel,
           saves it (to the JSON file) and prints the id
           If the class name is missing, print a message
           If the class name doesn’t exist, print a message
        """
        if not argument:
            print("** class name missing ** ")
        if not argument in class_names:
            print("** class doesn't exist ** ")
        else:
            new_instance = class_names[argument]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, argument):
        """
        Prints the string representation of an instance,
        based on the class name and id
        """
        if not argument:
            print("** class name missing ** ")
        else:
            args = argument.split(" ")
            if args[0] not in class_names:
                 print("** class doesn't exist ** ")
            elif len(args) < 2:
                print("** instance id missing ** ")
            else:
                key = args[0] + "." + args[1]
                




"""prevents execution when code is imported"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()