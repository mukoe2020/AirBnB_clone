#!/usr/bin/python3

import cmd
import models

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

"""prevents execution when code is imported"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()