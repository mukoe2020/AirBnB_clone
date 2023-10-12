#!/usr/bin/python3

import cmd
from gc import get_objects
import models
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Contains the entry point of the command interpreter."""

    prompt = "(hbnb) "

    class_names = {
        'BaseModel': BaseModel,
        'User': User
    }

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
        Creates a new instance of a class, saves it to the JSON file, and prints the ID.
        If the class name is missing or doesn't exist, it prints a message.
        """
        if not argument:
            print("Class name missing")
        elif argument not in self.class_names:
            print("Class doesn't exist")
        else:
            new_instance = self.class_names[argument]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, argument):
        """
        Prints the string representation of an instance based on the class name and ID.
        """
        if not argument:
            print("Class name missing")
        else:
            args = argument.split(" ")
            if args[0] not in self.class_names:
                print("Class doesn't exist")
            elif len(args) < 2:
                print("Instance ID missing")
            else:
                objs = models.storage.all()
                key = f"{args[0]}.{args[1]}"
                if key in objs.keys():
                    print(objs[key])
                else:
                    print("No instance found")

    def do_destroy(self, argument):
        """Deletes an instance based on the class name and ID (saves the change into the JSON file)"""
        if not argument:
            print("Class name missing")
        else:
            args = argument.split(" ")
            if args[0] not in self.class_names:
                print("Class doesn't exist")
            elif len(args) < 2:
                print("Instance ID missing")
            else:
                objs = models.storage.all()
                key = f"{args[0]}.{args[1]}"
                if key in objs.keys():
                    del objs[key]
                    models.storage.save()
                else:
                    print("No instance found")

    def do_all(self, argument):
        objs = models.storage.all()

        if not argument:
            print([str(obj) for obj in objs.values()])
        else:
            args = argument.split(" ")
            if args[0] not in self.class_names:
                print("Class doesn't exist")
            else:
                class_name = args[0]
                print([str(obj) for obj in objs.values() if obj.__class__.__name__ == class_name])

    def do_update(self, argument):
        args = argument.split(" ")

        if not argument:
            print("Class name missing")
        elif args[0] not in self.class_names:
            print("Class doesn't exist")
        elif len(args) < 2:
            print("Instance ID missing")
        else:
            obj_key = f"{args[0]}.{args[1]}"
            objs = models.storage.all()
            if obj_key in objs.keys():
                if len(args) < 3:
                    print("Attribute name missing")
                elif len(args) < 4:
                    print("Value missing")
                else:
                    instance = objs[obj_key]
                    setattr(instance, args[2], args[3])
                    instance.save()
            else:
                print("No instance found")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
